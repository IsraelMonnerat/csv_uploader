import os
import logging
import psycopg2
from typing import List, Tuple
from fastapi import HTTPException

from ...models.payloads.csv_uploader import AddItemPayload

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
        """
        Asynchronously establishes a connection to the database.

        This method attempts to connect to the database using the provided environment variables.
        If a connection cannot be established, an HTTPException with a status code of 500 and
        an error message is raised.

        Parameters:
            self (ResumeConnectionHandler): The instance of the ResumeConnectionHandler class.

        Returns:
            None: This method does not return anything.

        Raises:
            HTTPException: If a connection to the database cannot be established.
        """
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
        """
        Close the connection to the database.

        This method closes the connection to the database and sets the connection and cursor attributes to None.

        Parameters:
            self (ResumeConnectionHandler): The instance of the ResumeConnectionHandler class.

        Returns:
            None: This method does not return anything.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

        if self.cursor:
            self.cursor.close()
            self.cursor = None

    async def save_csv_file(self, data) -> None:
        """
        Asynchronously saves a CSV file into the 'users_data' table in the database.

        Args:
            data (List[List[str]]): The data to be inserted into the table. Each row should be a list of values in the order: nome, data_nascimento, genero, nacionalidade, data_criacao, data_atualizacao.

        Returns:
            None: This function does not return anything.

        Raises:
            HTTPException: If there is an error while saving the CSV file.

        """
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
            await self.close_connection()
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Failed to save CSV file. Error: {error}") from error
        return None

    async def get_all_values_with_pagination(self, page_number: int, page_size: int) -> List[Tuple]:
        """
        Asynchronously retrieves all values from the 'users_data' table in the database with pagination.

        Args:
            page_number (int): The page number to retrieve values from.

        Returns:
            List[Tuple]: A list of tuples representing the rows of the 'users_data' table. Each tuple contains the values of a row.

        Raises:
            HTTPException: If there is an error while retrieving the values.
        """
        offset = (page_number - 1) * page_size
        select_query = """
            SELECT * FROM users_data
            OFFSET %s
            LIMIT %s
        """
        try:
            self.cursor.execute(select_query, (offset, page_size))
            result = self.cursor.fetchall()
        except Exception as error:
            logging.error("Failed to get all values. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to get all values. Error: {error}") from error
        await self.close_connection()
        return result
    

    async def get_all_values(self) -> List[Tuple]:
        """
        Asynchronously retrieves all values from the 'users_data' table in the database.
        
        Returns:
            List[Tuple]: A list of tuples representing the rows of the 'users_data' table. Each tuple contains the values of a row.

        Raises:
            HTTPException: If there is an error while retrieving the values.
        """
        select_query = """
            SELECT * FROM users_data
        """
        try:
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
        except Exception as error:
            logging.error("Failed to get all values. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to get all values. Error: {error}") from error
        await self.close_connection()
        return result
    
  
    async def get_filtered_value(self, field_name: str, field_value: str, page: int = 1) -> List[Tuple]:
        """
        Asynchronously retrieves filtered values from the repository based on the given field name and value, with pagination.

        Args:
            field_name (str): The name of the field to filter by.
            field_value (str): The value to filter by.
            page (int, optional): The page number to retrieve. Defaults to 1.
            limit (int, optional): The maximum number of items per page. Defaults to 5.

        Returns:
            List[Tuple]: A list of tuples representing the filtered rows from the 'users_data' table, paginated.
        """
        offset = (page - 1) * 5
        select_query = f"""
            SELECT * FROM users_data
            WHERE {field_name} = '{field_value}'
            OFFSET {offset}
            LIMIT 5
        """
        try: 
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
        except Exception as error:
            logging.error("Failed to get filtered value. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to get filtered value. Error: {error}") from error
        await self.close_connection()
        return result
    

    async def add_value_to_db(self, data: AddItemPayload) -> List[Tuple]:
        insert_query = """
            INSERT INTO users_data (nome, data_nascimento, genero, nacionalidade, data_criacao, data_atualizacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        inserted_id = None
        try:
            self.cursor.execute(
                insert_query,
                (data.nome,
                format_date(data.data_nascimento),
                 data.genero,
                 data.nacionalidade,
                 format_date(data.data_criacao),
                 format_date(data.data_atualizacao))
            )
            inserted_id = self.cursor.fetchone()[0]
            self.connection.commit()
        except Exception as error:
            logging.error("Failed to add value to DB. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to add value to DB. Error: {error}") from error
        logging.info("Value added to DB")
        await self.close_connection()
        return await self.get_filtered_value("id", inserted_id)
    

    async def update_value_in_db(self, data: AddItemPayload, item_id: int) -> List[Tuple]:
        """
        Asynchronously updates a value in the 'users_data' table in the database.

        Args:
            data (AddItemPayload): The data containing the updated values for the row.
            item_id (int): The ID of the row to be updated.

        Returns:
            List[Tuple]: A list of tuples containing the updated row, with the 'id' field as the first element.

        Raises:
            HTTPException: If there is an error while updating the value in the database.

        """
        update_query = """
            UPDATE users_data
            SET nome = %s, data_nascimento = %s, genero = %s, nacionalidade = %s, data_criacao = %s, data_atualizacao = %s
            WHERE id = %s
        """
        try:
            self.cursor.execute(
                update_query,
                (data.nome,
                 format_date(data.data_nascimento),
                 data.genero,
                 data.nacionalidade,
                 format_date(data.data_criacao),
                 format_date(data.data_atualizacao),
                 item_id)
            )
            self.connection.commit()
        except Exception as error:
            logging.error("Failed to update value in DB. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to update value in DB. Error: {error}") from error
        logging.info("Value updated in DB")
        await self.close_connection()
        return await self.get_filtered_value("id", item_id)


    async def delete_value_from_db(self, item_id: int) -> None:
        """
        Asynchronously deletes a value from the 'users_data' table in the database.

        Args:
            item_id (int): The ID of the row to be deleted.

        Raises:
            HTTPException: If there is an error while deleting the value from the database.

        """
        delete_query = "DELETE FROM users_data WHERE id = %s"
        try:
            self.cursor.execute(delete_query, (item_id,))
            self.connection.commit()
        except Exception as error:
            logging.error("Failed to delete value from DB. Error: %s", error)
            raise HTTPException(status_code=500, detail=f"Failed to delete value from DB. Error: {error}") from error
        logging.info("Value deleted from DB")
        await self.close_connection()