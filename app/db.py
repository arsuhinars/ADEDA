from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app import config

engine = create_engine(
    config.DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
