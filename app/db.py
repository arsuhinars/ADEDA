from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import app.config as config

engine = create_engine(
    config.DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
