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
