import json

from pydantic import BaseModel, Json, validator


class SInspection(BaseModel):
    device_id: int
    data: Json

    @validator('data', pre=True)
    def format_json(cls, data):
        if isinstance(data, dict):
            return json.dumps(data)
        return data

    class Config:
        orm_mode = True


class SInspectionFull(BaseModel):
    id: int
    image_path: str | None
    pdf_path: str | None
    device_id: int
    data: Json
    telegram_id: str | None

    @validator('data', pre=True)
    def format_json(cls, data):
        if isinstance(data, dict):
            return json.dumps(data)
        return data

    class Config:
        orm_mode = True
