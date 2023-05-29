import datetime
import shutil
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile
from pydantic import Json

from app.auth.scheme import get_token
from app.devices.dao import DevicesDAO
from app.devices.models import Devices
from app.inspections.dao import InspectionsDAO
from app.inspections.models import Inspections
from app.inspections.schemas import SInspectionFull
from app.logger import logger
from app.tasks.tasks import process_pic, write_pdf

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
        image: Optional[UploadFile],
        token: str = Depends(get_token),
) -> SInspectionFull:
    logger.info(f"Created inspection", extra={"token": token, "new_inspection": data})

    device: Devices = await DevicesDAO.find_by_id(device_id)
    inspection: Inspections = await InspectionsDAO.add(
        device_id=device_id,
        data=data,
    )

    im_path = f"app/static/images/{inspection.id}.png"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)

    process_pic.delay(im_path)

    pdf_path = f"app/static/pdf/{inspection.id}.pdf"
    write_pdf.delay(
        inspection_id=inspection.id,
        device_name=device.name,
        data=data,
        image=im_path,
        output=pdf_path,
    )
    inspection: Inspections = await InspectionsDAO.update_by_id(
        inspection.id, pdf_path=pdf_path, image_path=im_path
    )

    return inspection
