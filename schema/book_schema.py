from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    id: Optional[int]
    nombre: str
    descripcion: str
    propietario: str