# from fastapi import APIRouter, UploadFile
# import shutil
#
# from app.tasks.tasks import process_pic
#
# router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


# @router.post(
#     "/devices",
#     status_code=201,
#     description="Загрузка фото устройства с идентификатором исследования",
# )
# async def add_device_image(device_id: int, inspection_id: int, file: UploadFile):
#     im_path = f"app/static/images/{device_id}_{inspection_id}.png"
#     with open(im_path, "wb+") as file_object:
#         shutil.copyfileobj(file.file, file_object)
#     process_pic.delay(im_path)
