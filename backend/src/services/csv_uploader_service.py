import csv
import logging
from io import StringIO
from typing import List, Tuple, Union

from fastapi import UploadFile

from fastapi.responses import StreamingResponse

from ..utils import format_date_ymd_to_ymd

from ..models.payloads.csv_uploader import AddItemPayload

from ..infra.cv_uploader_data_base.csv_uploader_repository import ResumeConnectionHandler
from ..models.responses.csv_uploader import (
    CsvUploaderResponse,
    CsvUploaderResponseAllItems,
)


class CsvUploaderService:
    def __init__(self):
        logging.info("Initializing CSV uploader service")
        self.repository = ResumeConnectionHandler()

    async def upload_csv(self, file: UploadFile) -> CsvUploaderResponse:
        """
        Asynchronously uploads a CSV file, reads the file content, saves it to the database, and returns a CsvUploaderResponse with a success message.

        Parameters:
            file (UploadFile): The CSV file to be uploaded.

        Returns:
            CsvUploaderResponse: A response object indicating the success of the CSV file upload.
        """
        file_content = file.file.read().decode("utf-8")
        reader = csv.reader(file_content.splitlines())
        await self.repository()
        await self.repository.save_csv_file(list(reader))
        return CsvUploaderResponse(message="CSV file uploaded successfully")

    async def get_all_values_with_pagination(self, page_number: int, page_size: int = 10) -> List[CsvUploaderResponseAllItems] | None:
        """
        Asynchronously retrieves all values from the database with pagination.

        Parameters:
            page_number (int): The page number to retrieve values from.

        Returns:
            List[CsvUploaderResponseAllItems] | None: A list of CsvUploaderResponseAllItems objects, or None if no values are found.
        """
        logging.info("Getting all values with pagination")
        await self.repository()
        values, total_count = await self.repository.get_all_values_with_pagination(page_number, page_size)
        if not values:
            return None
        return await self.prepare_values(values), total_count

    async def get_filtered_value(self, field_name: str, field_value: str, page: int) -> List[CsvUploaderResponseAllItems] | None:
        """
        Asynchronously retrieves filtered values from the repository based on the given field name and value.

        Args:
            field_name (str): The name of the field to filter by.
            field_value (str): The value to filter by.

        Returns:
            List[CsvUploaderResponseAllItems] | None: A list of CsvUploaderResponseAllItems objects if values are found, 
            otherwise None.
        """
        await self.repository()
        values = await self.repository.get_filtered_value(field_name, field_value, page)
        if not values:
            return None
        return await self.prepare_values(values)

    @staticmethod
    async def prepare_values(values: Union[List[Tuple], Tuple]) -> List[CsvUploaderResponseAllItems]:
        """
        Asynchronously prepares a list of values from a list of tuples or a single tuple into a list of CsvUploaderResponseAllItems objects.

        Args:
            values (Union[List[Tuple], Tuple]): The list of tuples or a single tuple containing the values to be prepared.

        Returns:
            List[CsvUploaderResponseAllItems]: The list of prepared CsvUploaderResponseAllItems objects.
        """
        prepared_values = []
        if isinstance(values, tuple):
            values = [values]

        for value in values:
            prepared_value = {
                "id": int(value[0]),
                "nome": str(value[1]),
                "data_nascimento": format_date_ymd_to_ymd(str(value[2])),
                "genero": str(value[3]),
                "nacionalidade": str(value[4]),
                "data_criacao": format_date_ymd_to_ymd(str(value[5])),
                "data_atualizacao": format_date_ymd_to_ymd(str(value[6])),
            }
            prepared_values.append(prepared_value)

        return [CsvUploaderResponseAllItems(**value) for value in prepared_values]

    async def add_item(self, payload: AddItemPayload) -> List[CsvUploaderResponseAllItems]:
        """
        Asynchronously adds an item to the repository and returns a list of prepared values.

        Args:
            payload (AddItemPayload): The payload containing the item to be added.

        Returns:
            List[CsvUploaderResponseAllItems]: A list of prepared values.
        """
        await self.repository()
        added_value = await self.repository.add_value_to_db(payload)
        return await self.prepare_values(added_value)

    async def update_item(self, payload: AddItemPayload, item_id: int) -> List[CsvUploaderResponseAllItems]:
        """
        Asynchronously updates an item in the repository and returns a list of prepared values.

        Args:
            payload (AddItemPayload): The payload containing the updated item.
            item_id (int): The ID of the item to be updated.

        Returns:
            List[CsvUploaderResponseAllItems]: A list of prepared values.
        """
        await self.repository()
        updated_value = await self.repository.update_value_in_db(payload, item_id)
        return await self.prepare_values(updated_value)

    async def delete_item(self, item_id: int) -> None:
        """
        Asynchronously deletes an item from the repository.

        Args:
            item_id (int): The ID of the item to be deleted.
        """
        await self.repository()
        await self.repository.delete_value_from_db(item_id)

    
    
    async def get_csv_file(self) -> StreamingResponse:
        """
        Asynchronously downloads the CSV file from the repository.
        """
        await self.repository()
        all_values = await self.repository.get_all_values()
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)

        csv_writer.writerow(["Nome", "Data de Nascimento", "Gênero", "Nacionalidade", "Data de Criacao", "Data de Atualizacao"])
        
        for row in all_values:
            csv_writer.writerow(row[1:])

        csv_buffer.seek(0)

        response = StreamingResponse(csv_buffer, media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=relatorio.csv"
        response.headers["Content-Type"] = "text/csv; charset=utf-8"

        return response
