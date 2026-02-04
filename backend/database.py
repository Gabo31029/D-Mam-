
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Supabase PostgreSQL URL
# Example: postgresql://postgres.xxxx:password@aws-0-region.pooler.supabase.com:6543/postgres
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback only for local dev if explicitly needed, but per requirements we target Supabase
    # Warning user or default to sqlite for safety if env not set, but goal is Postgres.
    SQLALCHEMY_DATABASE_URL = "sqlite:///./recetario.db"

if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
else:
    # Postgres connection
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
