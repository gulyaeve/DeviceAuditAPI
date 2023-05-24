from pydantic import BaseModel
from pydantic.types import Json


class SInspection(BaseModel):
    device_id: int
    data: Json

    class Config:
        orm_mode = True
