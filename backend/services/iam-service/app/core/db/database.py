from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy_utils import database_exists, create_database
from loguru import logger

from app.core.config import get_settings

config = get_settings()

DATABASE_URL = (
    f"{config.DATABASE_DIALECT}://"
    f"{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@"
    f"{config.DATABASE_HOSTNAME}:{config.DATABASE_PORT}/"
    f"{config.DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL, echo=config.DEBUG_MODE, future=True)
Base = declarative_base()

try:
    if not database_exists(engine.url):
        logger.info("Creating database...")
        create_database(engine.url)
        logger.info(" Database created successfully")
except Exception as e:
    logger.error(f" Error creating database: {e}")

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
logger.info(" Database session configured")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as ex:
        logger.error(f" Database error: {ex}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    from app.domain.models import user  
    Base.metadata.create_all(bind=engine)
