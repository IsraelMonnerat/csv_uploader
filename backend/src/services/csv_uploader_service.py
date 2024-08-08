import csv
import logging
from typing import List, Tuple

from fastapi import UploadFile

from ..infra.cv_uploader_data_base.csv_uploader_repository import ResumeConnectionHandler
from ..models.responses.csv_uploader import (
    CsvUploaderResponse,
    ListResponseAllItems,
    CsvUploaderResponseAllItems,
)


class CsvUploaderService:
    def __init__(self):
        logging.info("Initializing CSV uploader service")
        self.repository = ResumeConnectionHandler()

    async def upload_csv(self, file: UploadFile) -> CsvUploaderResponse:
        file_content = file.file.read().decode("utf-8")
        reader = csv.reader(file_content.splitlines())
        await self.repository()
        await self.repository.save_csv_file(list(reader))
        return CsvUploaderResponse(message="CSV file uploaded successfully")

    async def get_all_values_with_pagination(self, page_number: int) -> List[CsvUploaderResponseAllItems] | None:
        logging.info("Getting all values with pagination")
        await self.repository()
        values = await self.repository.get_all_values_with_pagination(page_number)
        if not values:
            return None
        prepared_values = []
        for value in values:
            prepared_value = {
                "nome": str(value[1]),
                "data_nascimento": str(value[2]),
                "genero": str(value[3]),
                "nacionalidade": str(value[4]),
                "data_criacao": str(value[5]),
                "data_atualizacao": str(value[6]),
            }
            prepared_values.append(prepared_value)

        return [CsvUploaderResponseAllItems(**value) for value in prepared_values]


