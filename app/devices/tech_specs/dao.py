from app.dao.base import BaseDAO
from app.devices.tech_specs.models import TechSpecs


class TechSpecsDAO(BaseDAO):
    model = TechSpecs
