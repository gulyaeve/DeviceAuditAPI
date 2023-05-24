from sqlalchemy import Column, Integer, String

from app.database import Base


class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
