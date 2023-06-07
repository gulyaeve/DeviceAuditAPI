import os

from app.config import settings
from app.tasks.celery_config import celery
from PIL import Image
from pathlib import Path
from json2html import json2html
from pyhtml2pdf import converter


html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>HELLO</title>
</head>
<body>
<h1>Экспертиза устройства: {device_name}</h1>
{table}
{image}
</body>
</html>
"""


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im.thumbnail((600, 600), Image.Resampling.LANCZOS)
    im.save(f"{settings.STATIC_DIR}/images/{im_path.name}")


@celery.task
def write_pdf(
        inspection_id: int,
        device_name: str,
        data: dict,
        output: str,
        image: str = "",
):
    if image:
        img = f"<h2>Изображение устройства:</h2>" \
              f"<img src=\"{os.path.abspath(image)}\" width=300>"
    else:
        img = ""

    table = json2html.convert(json=data)
    for item in table.split("</td>"):
        if "FAILED" in item:
            item_color = item.replace("<td>", "<td bgcolor=\"red\">")
            item_without_result = item_color.replace("FAILED", "")
            table = table.replace(item, item_without_result)
        if "PASSED" in item:
            item_color = item.replace("<td>", "<td bgcolor=\"green\">")
            item_without_result = item_color.replace("PASSED", "")
            table = table.replace(item, item_without_result)

    with open(f"{settings.STATIC_DIR}/html/{inspection_id}.html", "w") as html:
        html.write(
            html_template.format(
                device_name=device_name,
                table=table,
                image=img,
            )
        )
    path = os.path.abspath(f'{settings.STATIC_DIR}/html/{inspection_id}.html')
    converter.convert(f'file:///{path}', output)
    # os.remove(path)
