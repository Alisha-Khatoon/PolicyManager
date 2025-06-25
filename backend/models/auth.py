from sqlalchemy import Column, String
from backend.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)