from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from backend.db.session import Base
from sqlalchemy.orm import relationship # Add this import
from backend.models.policy import Policy

class Enterprise(Base):
    __tablename__ = "enterprises"
    __table_args__ = {'schema': 'public'}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    industry = Column(String(100), nullable=False, index=True)
    google_id = Column(String(255), unique=True, index=True)
    policies = relationship("Policy", back_populates="enterprise")
