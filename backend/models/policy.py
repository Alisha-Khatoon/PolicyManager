import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSON, UUID  
from sqlalchemy.sql import func
from backend.db.session import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# from sqlalchemy.dialects.postgresql import UUID

class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Replace Integer    
    filename = Column(String(255), index=True)  # Added index for faster lookups
    size = Column(Integer)
    content = Column(Text)
    analysis = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    ai_review = Column(Text, nullable=True)
    insights = Column(JSON, nullable=True)  
    category = Column(String(100), index=True, nullable=True)  # Added index
    industry = Column(String(100), nullable=True)
    enterprise_id = Column(UUID(as_uuid=True), ForeignKey('public.enterprises.id'), index=True) #
    enterprise = relationship("Enterprise", back_populates="policies")
    user_id = Column(String)
    # Simplify table args unless you need GIN
    __table_args__ = {'extend_existing': True}

    # Recommended for PostgreSQL full-text search:
    