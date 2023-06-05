import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI

# from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis

# from sqladmin import Admin

# from app.admin.auth import authentication_backend
# from app.admin.views import UserAdmin
from app.config import settings
from app.database import engine
from app.logger import logger
from app.users.router import router as users_router
from app.devices.router import router as devices_router
from app.tech_specs.router import router as tech_specs_router
from app.inspections.router import router as inspections_router

# from app.pages.router import router as pages_router
# from app.images.router import router as images_router
# from app.importer.router import router as import_router

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
)

app = FastAPI()

# app.include_router(users_router)
app.include_router(devices_router)
app.include_router(tech_specs_router)
app.include_router(inspections_router)
# app.include_router(pages_router)
# app.include_router(images_router)
# app.include_router(import_router)

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}",
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

# admin = Admin(app, engine, authentication_backend=authentication_backend)
# admin.add_view(UserAdmin)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     # При подключении Prometheus + Grafana подобный лог не требуется
#     logger.info("Request handling time", extra={
#         "process_time": round(process_time, 4)
#     })
#     return response


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        settings.redis_url, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# instrumentator = Instrumentator(
#     should_group_status_codes=False,
#     excluded_handlers=[".*admin.*", "/metrics"],
# )
# instrumentator.instrument(app).expose(app)
