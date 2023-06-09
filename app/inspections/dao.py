import re

from pydantic import json
from sqlalchemy import insert

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.devices.dao import DevicesDAO
from app.tech_specs.dao import TechSpecsDAO
from app.tech_specs.models import TechSpecs
from app.exceptions import EntityNotExistsException, InspectionValidateException
from app.inspections.models import Inspections
from app.inspections.utils import validate_to_reference
from app.logger import logger


class InspectionsDAO(BaseDAO):
    model = Inspections

    @classmethod
    async def add(cls, device_id: int, data: json, telegram_id: str | None):
        device = await DevicesDAO.find_one_or_none(id=device_id)
        if device:
            tech_specs: list[TechSpecs] = await TechSpecsDAO.find_all(device_id=device_id)
            tech_specs_list = [tech_spec.description for tech_spec in tech_specs]
            if tech_specs_list == list(data.keys()):

                # Проверка по референсным значениям
                for index, (key, value) in enumerate(data.items()):
                    reference = tech_specs[index].reference_value
                    validation = validate_to_reference(value, reference)
                    if validation is not None:
                        if validation is True:
                            data[key] += f" ({reference}) PASSED"
                        else:
                            data[key] += f" ({reference}) FAILED"

                async with async_session_maker() as session:
                    query = (
                        insert(cls.model)
                        .values(
                            device_id=device_id,
                            data=data,
                            telegram_id=telegram_id,
                        )
                        .returning(cls.model)
                    )
                    result = await session.execute(query)
                    await session.commit()
                    logger.info(
                        f"Inserted inspection for device [{device_id}]",
                        extra={"telegram_id": telegram_id, "data": data}
                    )
                    return result.scalars().one()
            else:
                raise InspectionValidateException
        else:
            raise EntityNotExistsException

