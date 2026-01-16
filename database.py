from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#* Zegt waar de database zich bevindt
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

#* De engine maakt verbinding met de database, SQLite gebruikt maar één thread
#* maar fastapi kan meerdere threads gebruiken, dus moet check_same_thread op False
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

#* Maakt een sessionmaker aan die gebruikt wordt om sessies te maken
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#* Nieuwe manier om een basisklasse voor alle ORM modellen te maken
class Base(DeclarativeBase):
    pass

#* Dependency functie om een database sessie te krijgen
def get_db():
    with SessionLocal() as db:
        yield db
