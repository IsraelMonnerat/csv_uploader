import logging
from typing import List

from fastapi import (
    APIRouter,
    Request,
    File,
    UploadFile
)
from fastapi.responses import StreamingResponse

from ..models.payloads.csv_uploader import AddItemPayload

from ..services.csv_uploader_service import CsvUploaderService
from ..models.responses.csv_uploader import (
    CsvUploaderResponse,
    CsvUploaderResponseAllItems,
)

router = APIRouter(tags=["CSV Uploader"])

@router.post("/upload-csv-file")
async def upload_csv(file: UploadFile = File(...)) -> CsvUploaderResponse:
    logging.info("Uploading CSV file")
    service = CsvUploaderService()
    return await service.upload_csv(file)


@router.post("/add-item")
async def add_item(payload: AddItemPayload) -> CsvUploaderResponseAllItems:
    logging.info("Adding item to DataBase")
    payload.validate_fields(payload.data_nascimento, payload.data_criacao, payload.data_atualizacao)
    service = CsvUploaderService()
    item = await service.add_item(payload)
    return item[0]


@router.get("/all")
async def get_all_values(request: Request) -> List[CsvUploaderResponseAllItems] | None:
    logging.info("Getting all values")
    page_size = request.headers.get("page_size", 10)
    page_number = request.headers.get("page", 1)
    service = CsvUploaderService()
    response = await service.get_all_values_with_pagination(int(page_number), int(page_size))
    if response:
        return response
    return None


@router.put("/update/id/{item_id}")
async def update_item(payload: AddItemPayload, item_id: int) -> CsvUploaderResponseAllItems:
    logging.info("Updating item. ID: %s", item_id)
    payload.validate_fields(payload.data_nascimento, payload.data_criacao, payload.data_atualizacao)
    service = CsvUploaderService()
    item = await service.update_item(payload, item_id)
    return item[0]


@router.delete("/delete/id/{item_id}", status_code=204)
async def delete_item(item_id: int) -> None:
    logging.info("Deleting item. ID: %s", item_id)
    service = CsvUploaderService()
    await service.delete_item(item_id)


@router.get("/filter/field/{field}/value/{value}")
async def get_value_by_field(request: Request, field: str, value: str) -> List[CsvUploaderResponseAllItems] | None:
    logging.info("Getting value by field. Field: %s, Value: %s", field, value)
    page_number = request.headers.get("page", 1)
    service = CsvUploaderService()
    response = await service.get_filtered_value(field, value, int(page_number))
    if response:
        return response
    return None


@router.get("/csv-file")
async def get_csv_file() -> StreamingResponse:
    logging.info("Getting CSV file")
    service = CsvUploaderService()
    return await service.get_csv_file()


