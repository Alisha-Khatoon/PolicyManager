from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://policy_app:securepassword@localhost:5432/policies")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Import all models here to ensure they are registered with SQLAlchemy
    from backend.models.enterprise import Enterprise
    from backend.models.auth import User
    from backend.models.policy import Policy
    
    print("Dropping and recreating all database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")