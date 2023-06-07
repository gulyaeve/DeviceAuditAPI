from fastapi import APIRouter, Depends

from app.auth.scheme import get_token
from app.tech_specs.dao import TechSpecsDAO
from app.tech_specs.schemas import STechSpec, STechSpecForImport
from app.logger import logger

router = APIRouter(
    prefix="/tech_specs",
    tags=["Технические спецификации устройств"]
)


@router.get(
    "",
    status_code=200,
    description="Получение спецификаций устройств",
)
async def get_tech_specs(
        tech_spec_id: int | None = None,
        device_id: int | None = None,
        token: str = Depends(get_token),
) -> list[STechSpec]:
    if tech_spec_id:
        logger.info(f"Get tech spec by [{tech_spec_id}]", extra={"token": token})
        tech_spec = await TechSpecsDAO.find_by_id(tech_spec_id)
        return [tech_spec]
    elif device_id:
        logger.info(f"Get tech specs for device id [{device_id}]", extra={"token": token})
        tech_specs = await TechSpecsDAO.find_all(device_id=device_id)
        return tech_specs
    else:
        logger.info(f"Get tech specs", extra={"token": token})
        tech_specs = await TechSpecsDAO.find_all()
        return tech_specs


@router.post(
    "",
    status_code=201,
    description="Запись технических спецификаций для устройства",
)
async def add_tech_specs(device_id: int, tech_specs: list[STechSpecForImport], token: str = Depends(get_token)):
    logger.info(f"Created tech specs for device_id[{device_id}]", extra={"token": token, "tech_specs": tech_specs})
    for tech_spec in tech_specs:
        await TechSpecsDAO.add(
            device_id=device_id,
            description=tech_spec.description,
            reference_value=tech_spec.reference_value,
        )
