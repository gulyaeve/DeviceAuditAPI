from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TechSpecs(Base):
    __tablename__ = "tech_specs"

    id = Column(Integer, primary_key=True)
    device_id = Column(ForeignKey("devices.id"))
    description = Column(String, unique=True, nullable=False)
    reference_value = Column(String, nullable=True)

    device = relationship("Devices", back_populates="tech_specs")

