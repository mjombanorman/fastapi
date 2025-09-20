from fastapi import Depends
from typing_extensions import Annotated
from sqlmodel import SQLModel
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(
    url=settings.POSTGRES_URL(),
    echo=True,
   
)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_sessionmaker(bind=engine,
                                  expire_on_commit=False)() as session:
        yield session

SessionDep=Annotated[AsyncSession, Depends(get_session)]