from sqlalchemy import Column, Integer, JSON, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.devices.models import Devices


class Inspections(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True)
    image_path = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)
    device_id = Column(ForeignKey(f"{Devices.__tablename__}.id"))
    data = Column(JSON)
    telegram_id = Column(String, nullable=True)

    device = relationship("Devices", back_populates=__tablename__)

    def __repr__(self):
        return f"Inspection(id={self.id!r}, " \
               f"image_path={self.image_path!r}, " \
               f"pdf_path={self.pdf_path!r}, " \
               f"device_id={self.device_id!r}, " \
               f"data={self.data!r}, " \
               f"telegram_id={self.telegram_id!r})"

