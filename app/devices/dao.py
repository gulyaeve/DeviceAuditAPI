from app.dao.base import BaseDAO
from app.devices.models import Devices


class DevicesDAO(BaseDAO):
    model = Devices
