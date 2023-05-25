from app.tasks.celery_config import celery
from PIL import Image
from pathlib import Path


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im.thumbnail((600, 600), Image.Resampling.LANCZOS)
    im.save(f"app/static/images/{im_path.name}")
