from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException


class AddItemPayload(BaseModel):
    nome: str
    data_nascimento: str
    nacionalidade: str
    genero: str
    data_criacao: str
    data_atualizacao: str

    @classmethod
    def validate_date_format(cls, value) -> None:
        try:
            datetime.strptime(value, '%Y/%m/%d')
        except ValueError:
            try:
                datetime.strptime(value, '%d/%m/%Y')
            except ValueError as error:
                raise HTTPException(status_code=400, detail=f"Invalid field format: {value}") from error

        
    @classmethod
    def validate_fields(cls, data_nascimento: str, data_criacao: str, data_atualizacao: str) -> None:
        cls.validate_date_format(data_nascimento)
        cls.validate_date_format(data_criacao)
        cls.validate_date_format(data_atualizacao)
