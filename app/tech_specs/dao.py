from app.dao.base import BaseDAO
from app.tech_specs.models import TechSpecs


class TechSpecsDAO(BaseDAO):
    model = TechSpecs
