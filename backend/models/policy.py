from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from backend.db.session import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    size = Column(Integer)
    content = Column(Text)
    analysis = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    ai_review = Column(Text, nullable=True)