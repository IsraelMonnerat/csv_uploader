import os
import logging
import psycopg2
from typing import List, Tuple
from fastapi import HTTPException

from ..db_connection_handler import DbConnectionHandler

from ...utils import format_date


class ResumeConnectionHandler(DbConnectionHandler):
    def __init__(self):
        super().__init__()
        self.cursor = None
        self.connection = None

    async def __call__(self):
        await self.get_connection()

    async def get_connection(self) -> None:
        logging.info("Getting connection to database")
        try:
            self.connection = psycopg2.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port=os.environ.get("DB_PORT")
            )
        except Exception as error:
            logging.error("Failed to connect to database.  Error: %s", error)           
            raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to connect to database.  Error: {error}") from error

        self.cursor = self.connection.cursor()

    async def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

        if self.cursor:
            self.cursor.close()
            self.cursor = None

    async def save_csv_file(self, data) -> None:
        logging.info("Saving CSV file into DataBase")
        insert_query = """
            INSERT INTO users_data (nome, data_nascimento, genero, nacionalidade, data_criacao, data_atualizacao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            for row in data[1:]:
                nome, data_nascimento, genero, nacionalidade, data_criacao, data_atualizacao = row
                data_nascimento = format_date(data_nascimento)
                self.cursor.execute(insert_query, (nome, data_nascimento, genero, nacionalidade, data_criacao, data_atualizacao))
                self.connection.commit()
            self.close_connection()
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Failed to save CSV file. Error: {error}") from error
        return None

    async def get_all_values_with_pagination(self, page_number: int) -> List[Tuple]:
        offset = (page_number - 1) * 5
        select_query = """
            SELECT * FROM users_data
            OFFSET %s
            LIMIT 5
        """
        try:
            self.cursor.execute(select_query, (offset,))
            result = self.cursor.fetchall()
        except Exception as error:
            logging.error("Failed to get all values. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to get all values. Error: {error}") from error
        self.close_connection()
        return result
    
  
    async def get_filtered_value(self, field_name: str, field_value: str) -> Tuple:
        select_query = f"""
            SELECT * FROM users_data
            WHERE {field_name} = {field_value}
        """
        self.cursor.execute(select_query)
        result = self.cursor.fetchone()
        self.close_connection()
        return result
