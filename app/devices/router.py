from fastapi import APIRouter, Depends

from app.auth.scheme import get_token
from app.devices.dao import DevicesDAO
from app.devices.schemas import SDevices
from app.logger import logger

router = APIRouter(
    prefix="/devices",
    tags=["Устройства"],
)


@router.get(
    "",
    status_code=200,
    summary="Get devices list",
    description="Получение списка устройств"
)
async def get_devices(token: str = Depends(get_token)) -> list[SDevices]:
    logger.info("Get devices", extra={"token": token})
    devices = await DevicesDAO.find_all()
    return devices


@router.get("/{device_id}")
async def get_device(device_id: int, token: str = Depends(get_token)) -> SDevices:
    logger.info(f"Get device by id[{device_id}]", extra={"token": token})
    device = await DevicesDAO.find_by_id(device_id)
    return device


@router.post("", status_code=201)
async def create_device(name: str, token: str = Depends(get_token)):
    logger.info(f"Created device name[{name}]", extra={"token": token})
    device = await DevicesDAO.add(name=name)
    return device


@router.patch("/{device_id}", status_code=200)
async def change_device_name(
    device_id: int, new_name: str, token: str = Depends(get_token)
) -> SDevices:
    logger.info(
        f"Changed device id[{device_id}] name[{new_name}]", extra={"token": token}
    )
    device = await DevicesDAO.update_by_id(device_id, name=new_name)
    return device


@router.delete("", status_code=202)
async def delete_device(device_id: int, token: str = Depends(get_token)):
    logger.info(f"Deleted device id[{device_id}]", extra={"token": token})
    await DevicesDAO.delete(id=device_id)
