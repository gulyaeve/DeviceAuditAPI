from sqlalchemy import select, insert, delete, update, exc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.database import async_session_maker
from app.exceptions import DatabaseIntegrityError
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalars().one_or_none()
            except IntegrityError:
                logger.error(
                    "Database integrity error",
                    extra={"data": data},
                    exc_info=True
                )
                raise DatabaseIntegrityError
            except (SQLAlchemyError, Exception) as e:
                msg = ""
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc: Cannot add model"
                elif isinstance(e, Exception):
                    msg = "Unknown Exc: Cannot add model"
                extra = {"data": data}
                logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def update_by_id(cls, model_id: int, **data):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == model_id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalars().one_or_none()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
