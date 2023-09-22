from sqlalchemy import MetaData, Column, Integer, String, select, insert, delete, TEXT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, as_declarative

from create_bot import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    metadata = MetaData()


class UsersDB(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    phone = Column(String, nullable=True)


class AwardsDB(Base):
    __tablename__ = "awards"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    type_award = Column(String, nullable=False)
    title = Column(String, nullable=False)
    photo_id = Column(String, nullable=False)
    description = Column(TEXT, nullable=True)


class BaseDAO:
    """Класс взаимодействия с БД"""
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(1)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_many(cls, **filter_by) -> list:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).order_by(cls.model.id.asc())
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**data)
            await session.execute(stmt)
            await session.commit()


class UsersDAO(BaseDAO):
    model = UsersDB


class AwardsDAO(BaseDAO):
    model = AwardsDB

    @classmethod
    async def get_all(cls) -> list:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).order_by(cls.model.id.asc())
            result = await session.execute(query)
            return result.mappings().all()
