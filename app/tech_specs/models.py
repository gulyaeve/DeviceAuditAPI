from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.devices.models import Devices


class TechSpecs(Base):
    __tablename__ = "tech_specs"

    id = Column(Integer, primary_key=True)
    device_id = Column(ForeignKey(f"{Devices.__tablename__}.id"))
    description = Column(String, nullable=False)
    reference_value = Column(String, nullable=True)

    device = relationship("Devices", back_populates=__tablename__)

    def __repr__(self):
        return f"TechSpec(" \
               f"id={self.id!r}, " \
               f"device_id={self.device_id!r}, " \
               f"description={self.description!r}, " \
               f"reference_value={self.reference_value!r})"

