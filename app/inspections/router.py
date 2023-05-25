from fastapi import APIRouter, Depends

from app.auth.scheme import get_token
from app.inspections.dao import InspectionsDAO
from app.inspections.schemas import SInspection
from app.logger import logger

router = APIRouter(
    prefix="/inspections",
    tags=["Проведенные исследования"],
)


@router.get(
    "",
    status_code=200,
    description="Получение списка исследований",
)
async def get_inspections(token: str = Depends(get_token)) -> list[SInspection]:
    logger.info("Get inspections", extra={"token": token})
    inspections = await InspectionsDAO.find_all()
    return inspections


@router.get(
    "/{inspection_id}",
    status_code=200,
    description="Получение информации об исследовании",
)
async def get_inspection(inspection_id: int, token: str = Depends(get_token)) -> SInspection | None:
    logger.info(f"Get inspection by id[{inspection_id}]", extra={"token": token})
    inspection = await InspectionsDAO.find_by_id(inspection_id)
    return inspection


@router.post(
    "",
    status_code=201,
    description="Создание записи исследования",
)
async def create_inspection(new_inspection: SInspection, token: str = Depends(get_token)) -> SInspection:
    logger.info(f"Created inspection", extra={"token": token, "new_inspection": new_inspection})
    inspection = await InspectionsDAO.add(
        device_id=new_inspection.device_id,
        data=new_inspection.data,
    )
    return inspection
