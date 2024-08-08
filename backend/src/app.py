import logging
from fastapi import FastAPI

from .routers import csv_uploader


def add_routes(app: FastAPI) -> None:
    prefix = "/csv-uploader/api"
    app.include_router(csv_uploader.router, prefix=prefix)


def create_app() -> FastAPI:
    app = FastAPI(
        title="CSV Uploader",
        version="1.0.0",
        description="Upload your CSV with ease",
        docs_url="/docs",
    )
    logging.info("Adding routes")
    add_routes(app)
    return app


app = create_app()
