from typing import List
from pydantic import BaseModel, RootModel


class CsvUploaderResponse(BaseModel):
    message: str


class CsvUploaderResponseAllItems(BaseModel):
    id: int
    nome: str
    data_nascimento: str
    nacionalidade: str
    genero: str
    data_criacao: str
    data_atualizacao: str

class ListResponseAllItems(RootModel[List[CsvUploaderResponseAllItems]]):
    pass