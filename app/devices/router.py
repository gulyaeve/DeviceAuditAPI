from fastapi import APIRouter, Depends

from app.auth.scheme import get_token
from app.devices.dao import DevicesDAO
from app.devices.schemas import SDevices
from app.logger import logger

router = APIRouter(
    prefix="/devices",
    tags=["Устройства"],
)


@router.get("")
async def get_devices(token: str = Depends(get_token)) -> list[SDevices]:
    logger.info("Get devices", extra={
        "token": token
    })
    devices = await DevicesDAO.find_all()
    return devices


@router.post("")
async def create_device(name: str, token: str = Depends(get_token)):
    logger.info(f"Created device {name}", extra={
        "token": token
    })
    await DevicesDAO.add(name=name)
