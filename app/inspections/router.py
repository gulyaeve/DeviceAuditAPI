import datetime
import shutil

from fastapi import APIRouter, Depends, UploadFile
from pydantic import Json

from app.auth.scheme import get_token
from app.inspections.dao import InspectionsDAO
from app.inspections.schemas import SInspection, SInspectionFull
from app.logger import logger
from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/inspections",
    tags=["Проведенные исследования"],
)


@router.get(
    "",
    status_code=200,
    description="Получение списка исследований",
)
async def get_inspections(token: str = Depends(get_token)) -> list[SInspectionFull]:
    logger.info("Get inspections", extra={"token": token})
    inspections = await InspectionsDAO.find_all()
    return inspections


@router.get(
    "/{inspection_id}",
    status_code=200,
    description="Получение информации об исследовании",
)
async def get_inspection(inspection_id: int, token: str = Depends(get_token)) -> SInspectionFull | None:
    logger.info(f"Get inspection by id[{inspection_id}]", extra={"token": token})
    inspection = await InspectionsDAO.find_by_id(inspection_id)
    return inspection


@router.post(
    "",
    status_code=201,
    description="Создание записи исследования с фото",
)
async def create_inspection(
        device_id: int,
        data: Json,
        image: UploadFile,
        token: str = Depends(get_token),
) -> SInspection:
    logger.info(f"Created inspection", extra={"token": token, "new_inspection": data})
    im_path = f"app/static/images/{device_id}_{datetime.datetime.now()}.png"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
    process_pic.delay(im_path)

    inspection = await InspectionsDAO.add(
        device_id=device_id,
        image_path=im_path,
        data=data,
    )
    return inspection
