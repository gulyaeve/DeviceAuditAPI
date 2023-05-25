
from pydantic import json
from sqlalchemy import insert, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.devices.dao import DevicesDAO
from app.devices.tech_specs.dao import TechSpecsDAO
from app.exceptions import EntityNotExistsException, InspectionValidateException
from app.inspections.models import Inspections
from app.logger import logger


class InspectionsDAO(BaseDAO):
    model = Inspections

    @classmethod
    async def add(cls, device_id: int, data: json):
        device = await DevicesDAO.find_one_or_none(id=device_id)
        if device:
            tech_specs = await TechSpecsDAO.find_all(device_id=device_id)
            tech_specs_list = [tech_spec.description for tech_spec in tech_specs]
            if tech_specs_list == list(data.keys()):
                async with async_session_maker() as session:
                    query = (
                        insert(cls.model)
                        .values(
                            device_id=device_id,
                            data=data,
                        )
                        .returning(cls.model)
                    )
                    result = await session.execute(query)
                    await session.commit()
                    logger.info(f"Inserted inspection for device [{device_id}]", extra={"data": data})
                    return result.scalars().one()
            else:
                raise InspectionValidateException
        else:
            raise EntityNotExistsException

