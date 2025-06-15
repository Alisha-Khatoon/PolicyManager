from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True)
    password_hash = Column(String(255))  # For non-Gmail users
    is_google_auth = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    enterprise_id = Column(Integer, ForeignKey('enterprises.id'))
    # Add reset token fields
    reset_token = Column(String(255), unique=True)
    reset_token_expiry = Column(DateTime)

    enterprise = relationship("Enterprise", back_populates="users")

class Enterprise(Base):
    __tablename__ = 'enterprises'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="enterprise")
    policies = relationship("EnterprisePolicy", back_populates="enterprise")

class GovernmentPolicy(Base):
    __tablename__ = 'government_policies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(255))
    jurisdiction = Column(String(255))
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    related_updates = relationship("PolicyUpdate", back_populates="government_policy")

class EnterprisePolicy(Base):
    __tablename__ = 'enterprise_policies'
    
    id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('enterprises.id'))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    status = Column(String(50), default='active')  # active, archived, draft
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    enterprise = relationship("Enterprise", back_populates="policies")
    policy_updates = relationship("PolicyUpdate", back_populates="enterprise_policy")

class PolicyUpdate(Base):
    __tablename__ = 'policy_updates'
    
    id = Column(Integer, primary_key=True)
    enterprise_policy_id = Column(Integer, ForeignKey('enterprise_policies.id'))
    government_policy_id = Column(Integer, ForeignKey('government_policies.id'))
    previous_content = Column(Text, nullable=False)
    suggested_content = Column(Text, nullable=False)
    ai_analysis = Column(Text)
    similarity_score = Column(Float)
    status = Column(String(50), default='pending')  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = Column(DateTime)
    approved_by = Column(Integer, ForeignKey('users.id'))
    
    enterprise_policy = relationship("EnterprisePolicy", back_populates="policy_updates")
    government_policy = relationship("GovernmentPolicy", back_populates="related_updates")

# Database initialization
def init_db():
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session()

# Create database session
db = init_db()