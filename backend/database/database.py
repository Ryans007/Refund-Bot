from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database/database.db"
database_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
database_session = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
Base = declarative_base()

def get_db():
    """Gera uma sessão de banco de dados."""
    db = database_session()
    try:
        yield db
    finally:
        db.close()