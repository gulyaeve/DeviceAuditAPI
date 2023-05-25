from pydantic import BaseModel, Json


class SInspection(BaseModel):
    device_id: int
    data: Json

    class Config:
        orm_mode = True
