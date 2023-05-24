from pydantic import BaseModel


class STechSpec(BaseModel):
    description: str
    reference_value: str

    class Config:
        orm_mode = True
