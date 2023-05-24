from fastapi import APIRouter, Depends

from app.auth.scheme import get_token
from app.devices.router import router as devices_router
from app.devices.tech_specs.dao import TechSpecsDAO
from app.devices.tech_specs.schemas import STechSpec
from app.logger import logger

router = APIRouter(
    prefix=f"{devices_router.prefix}/tech_specs",
    tags=["Технические спецификации"]
)


@router.get(
    "/{device_id}",
    status_code=200,
    description="Получение списка спецификаций устройства",
)
async def get_tech_specs(device_id: int, token: str = Depends(get_token)) -> list[STechSpec]:
    logger.info(f"Get tech specs for device[{device_id}]", extra={"token": token})
    tech_specs = await TechSpecsDAO.find_all(device_id=device_id)
    return tech_specs


# @router.get(
#     "/{tech_spec_id}",
#     status_code=200,
#     description="Получение технической спецификации",
# )
# async def get_tech_spec(tech_spec_id: int, token: str = Depends(get_token)) -> STechSpec | None:
#     logger.info(f"Get tech spec by id[{tech_spec_id}]", extra={"token": token})
#     tech_spec = await TechSpecsDAO.find_by_id(tech_spec_id)
#     return tech_spec


@router.post(
    "",
    status_code=201,
    description="Запись технических спецификаций",
)
async def add_tech_specs(device_id: int, tech_specs: list[STechSpec], token: str = Depends(get_token)):
    logger.info(f"Created tech specs for device_id[{device_id}]", extra={"token": token, "tech_specs": tech_specs})
    for tech_spec in tech_specs:
        await TechSpecsDAO.add(
            device_id=device_id,
            description=tech_spec.description,
            reference_value=tech_spec.reference_value,
        )
