from pydantic import BaseModel


class SDevices(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
