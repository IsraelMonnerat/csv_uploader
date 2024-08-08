import logging
from typing import List, Tuple

from fastapi import (
    APIRouter, 
    Request,
    Response,
    File, 
    UploadFile
)
from fastapi.responses import HTMLResponse

from ..services.csv_uploader_service import CsvUploaderService
from ..models.responses.csv_uploader import (
    CsvUploaderResponse,
    ListResponseAllItems,
    CsvUploaderResponseAllItems,
)

router = APIRouter(tags=["CSV Uploader"])

@router.post("/upload-csv-file")
async def upload_csv(file: UploadFile = File(...)) -> CsvUploaderResponse:
    logging.info("Uploading CSV file")
    service = CsvUploaderService()
    return await service.upload_csv(file)


@router.get("/all")
async def get_all_values(request: Request) -> List[CsvUploaderResponseAllItems] | None:
    logging.info("Getting all values")
    page_number = request.headers.get("page", 1)
    service = CsvUploaderService()
    response = await service.get_all_values_with_pagination(int(page_number))
    if response:
        return response
    return None
