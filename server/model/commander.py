from pydantic import BaseModel


class Commander(BaseModel):
    nome: str
    url: str
