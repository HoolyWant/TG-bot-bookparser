import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession


BASE_DIR = Path(__file__).resolve().parent.parent.parent
dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)
DB_URL = (f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
          f"@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}")

async_engine = create_async_engine(
    url=DB_URL,
    echo=False,
)

Session = scoped_session(sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False))
async_session = Session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def async_register(session: AsyncSession, fullname):
    user = User(name=fullname)
    session.add(user)
    await session.commit()
