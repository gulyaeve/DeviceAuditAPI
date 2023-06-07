from pydantic import BaseModel


class STechSpec(BaseModel):
    id: int
    device_id: int
    description: str
    reference_value: str

    class Config:
        orm_mode = True


class STechSpecForImport(BaseModel):
    description: str
    reference_value: str

    class Config:
        orm_mode = True
