from app.dao.base import BaseDAO
from app.inspections.models import Inspections


class InspectionsDAO(BaseDAO):
    model = Inspections
