from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.devices.models import Devices


class Inspections(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True)
    device_id = Column(ForeignKey(f"{Devices.__tablename__}.id"))
    data = Column(JSON)

    device = relationship("Devices", back_populates=__tablename__)

    def __repr__(self):
        return f"Inspection(id={self.id!r}, device_id={self.device_id!r}, data={self.data!r})"

