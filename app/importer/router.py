import datetime
import shutil

from fastapi import APIRouter, UploadFile, Depends

from app.auth.scheme import get_token
from app.config import settings
from app.importer.utils import import_from_csv
from app.logger import logger

router = APIRouter(
    prefix="/import",
    tags=["Импорт"],
)


@router.post("/{table_name}", status_code=201)
async def import_csv(
    table_name: str, file: UploadFile, token: str = Depends(get_token)
):
    logger.info(f"Import {table_name}", extra={"token": token})
    file_path = f"{settings.STATIC_DIR}/csv/{table_name}_{datetime.datetime.now()}.csv"
    with open(file_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    await import_from_csv(table_name, file_path)

