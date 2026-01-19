""" Database configuratie en setup bestand """
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#* Zegt waar de database zich bevindt
# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

#* De engine maakt verbinding met de database, SQLite gebruikt maar één thread
#* maar fastapi kan meerdere threads gebruiken, dus moet check_same_thread op False
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
# )
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

#* Maakt een sessionmaker aan die gebruikt wordt om sessies te maken
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
asyncSessionLocal = async_sessionmaker(engine,
                                       class_=AsyncSession,
                                       expire_on_commit=False)


#* Nieuwe manier om een basisklasse voor alle ORM modellen te maken
class Base(DeclarativeBase):
    """ Basisklasse voor alle ORM modellen """
    pass

#* Dependency functie om een database sessie te krijgen
# def get_db():
#     with SessionLocal() as db:
#         yield db
async def get_db():
    """ Dependency functie om een database sessie te krijgen

    Yields:
        AsyncSession: Database sessie
    """
    async with asyncSessionLocal() as db:
        yield db
