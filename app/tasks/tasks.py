import os

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
    im.save(f"app/static/images/{im_path.name}")


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
            new_item = item.replace("<td>", "<td bgcolor=\"red\">")
            table = table.replace(item, new_item)
            table = table.replace("FAILED", "")
        if "PASSED" in item:
            new_item = item.replace("<td>", "<td bgcolor=\"green\">")
            table = table.replace(item, new_item)
            table = table.replace("PASSED", "")

    with open(f"app/static/html/{inspection_id}.html", "w") as html:
        html.write(
            html_template.format(
                device_name=device_name,
                table=table,
                image=img,
            )
        )
    path = os.path.abspath(f'app/static/html/{inspection_id}.html')
    converter.convert(f'file:///{path}', output)
    # os.remove(path)
