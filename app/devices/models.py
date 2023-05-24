from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    tech_specs = relationship("TechSpecs", back_populates="device")
