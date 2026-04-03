from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine=create_engine(DATABASE_URL)


session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()


def create_table():
    Base.metadata.create_all(engine)

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()

