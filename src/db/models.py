"""
Database models for HoloMesh Marketplace
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # user, designer, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    chips = relationship("Chip", back_populates="owner")
    transactions = relationship("Transaction", back_populates="user")
    collaborations = relationship("Collaboration", back_populates="initiator")

class Chip(Base):
    __tablename__ = "chips"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, default=0.0)
    royalty = Column(Float, default=0.0)  # Percentage for royalties
    designer = Column(String, nullable=False)
    ip_blocks = Column(Integer, default=1)
    serial_number = Column(String, unique=True, index=True)
    nft_id = Column(String, unique=True, index=True)
    zkp_protected = Column(Boolean, default=True)
    source_code = Column(Text)  # Protected by ZKP in real implementation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sales = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    
    # Foreign keys
    owner_id = Column(String, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="chips")
    designer_ids = Column(ARRAY(String))  # List of designer IDs who contributed IP blocks
    transactions = relationship("Transaction", back_populates="chip")
    collaborations = relationship("Collaboration", back_populates="chip")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chip_id = Column(String, ForeignKey("chips.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default="completed")  # pending, completed, failed
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chip = relationship("Chip", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

class Collaboration(Base):
    __tablename__ = "collaborations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chip_id = Column(String, ForeignKey("chips.id"), nullable=False)
    initiator_id = Column(String, ForeignKey("users.id"), nullable=False)
    collaborators = Column(ARRAY(String))  # List of user IDs
    status = Column(String, default="active")  # active, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    chip = relationship("Chip", back_populates="collaborations")
    initiator = relationship("User", back_populates="collaborations")

class DesignerProfile(Base):
    __tablename__ = "designer_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String)  # Processor, Memory, Interfaces, etc.
    experience_years = Column(Integer)
    projects_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)  # Average rating from 1-5
    bio = Column(Text)
    portfolio_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")

class ClientProfile(Base):
    __tablename__ = "client_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    company = Column(String)
    position = Column(String)
    preferences = Column(Text)  # JSON string of client preferences
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    designer_id = Column(String, ForeignKey("users.id"), nullable=False)  # Designer being subscribed to
    notification_frequency = Column(String, default="daily")  # immediate, daily, weekly
    auto_purchase = Column(Boolean, default=False)
    max_price = Column(Float)  # Maximum price for auto-purchase
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    designer = relationship("User", foreign_keys=[designer_id])

class VoiceCommand(Base):
    __tablename__ = "voice_commands"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    command = Column(Text, nullable=False)
    processed = Column(Boolean, default=False)
    response = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")