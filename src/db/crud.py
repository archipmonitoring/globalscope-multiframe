"""
CRUD operations for HoloMesh Marketplace database
"""
from sqlalchemy.orm import Session
from . import models
import uuid
from datetime import datetime
from typing import List, Optional

# User operations
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, email: str, hashed_password: str, role: str = "user"):
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, **kwargs):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in kwargs.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Chip operations
def get_chip(db: Session, chip_id: str):
    return db.query(models.Chip).filter(models.Chip.id == chip_id).first()

def get_chips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chip).offset(skip).limit(limit).all()

def get_chips_by_designer(db: Session, designer: str, skip: int = 0, limit: int = 100):
    return db.query(models.Chip).filter(models.Chip.designer == designer).offset(skip).limit(limit).all()

def create_chip(db: Session, name: str, description: str, price: float, royalty: float,
                designer: str, ip_blocks: int, serial_number: str, nft_id: str,
                zkp_protected: bool, source_code: str, owner_id: str, designer_ids: Optional[List[str]] = None):
    db_chip = models.Chip(
        name=name,
        description=description,
        price=price,
        royalty=royalty,
        designer=designer,
        ip_blocks=ip_blocks,
        serial_number=serial_number,
        nft_id=nft_id,
        zkp_protected=zkp_protected,
        source_code=source_code,
        owner_id=owner_id,
        designer_ids=designer_ids or []
    )
    db.add(db_chip)
    db.commit()
    db.refresh(db_chip)
    return db_chip

def update_chip(db: Session, chip_id: str, **kwargs):
    db_chip = get_chip(db, chip_id)
    if db_chip:
        for key, value in kwargs.items():
            setattr(db_chip, key, value)
        db.commit()
        db.refresh(db_chip)
    return db_chip

# Transaction operations
def get_transaction(db: Session, transaction_id: str):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).offset(skip).limit(limit).all()

def get_transactions_by_chip(db: Session, chip_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.chip_id == chip_id).offset(skip).limit(limit).all()

def create_transaction(db: Session, chip_id: str, user_id: str, price: float, status: str = "completed"):
    db_transaction = models.Transaction(
        chip_id=chip_id,
        user_id=user_id,
        price=price,
        status=status
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    # Update chip sales and revenue
    chip = get_chip(db, chip_id)
    if chip:
        chip.sales += 1
        chip.revenue += price
        db.commit()
        db.refresh(chip)
    return db_transaction

# Collaboration operations
def get_collaboration(db: Session, collaboration_id: str):
    return db.query(models.Collaboration).filter(models.Collaboration.id == collaboration_id).first()

def get_collaborations_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Collaboration).filter(models.Collaboration.initiator_id == user_id).offset(skip).limit(limit).all()

def create_collaboration(db: Session, chip_id: str, initiator_id: str, collaborators: List[str], status: str = "active"):
    db_collaboration = models.Collaboration(
        chip_id=chip_id,
        initiator_id=initiator_id,
        collaborators=collaborators,
        status=status
    )
    db.add(db_collaboration)
    db.commit()
    db.refresh(db_collaboration)
    return db_collaboration

# Designer Profile operations
def get_designer_profile(db: Session, profile_id: str):
    return db.query(models.DesignerProfile).filter(models.DesignerProfile.id == profile_id).first()

def get_designer_profile_by_user_id(db: Session, user_id: str):
    return db.query(models.DesignerProfile).filter(models.DesignerProfile.user_id == user_id).first()

def create_designer_profile(db: Session, user_id: str, specialization: Optional[str] = None, experience_years: int = 0,
                           projects_count: int = 0, rating: float = 0.0, bio: Optional[str] = None, portfolio_url: Optional[str] = None):
    db_profile = models.DesignerProfile(
        user_id=user_id,
        specialization=specialization,
        experience_years=experience_years,
        projects_count=projects_count,
        rating=rating,
        bio=bio,
        portfolio_url=portfolio_url
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Client Profile operations
def get_client_profile(db: Session, profile_id: str):
    return db.query(models.ClientProfile).filter(models.ClientProfile.id == profile_id).first()

def get_client_profile_by_user_id(db: Session, user_id: str):
    return db.query(models.ClientProfile).filter(models.ClientProfile.user_id == user_id).first()

def create_client_profile(db: Session, user_id: str, company: Optional[str] = None, position: Optional[str] = None, preferences: Optional[str] = None):
    db_profile = models.ClientProfile(
        user_id=user_id,
        company=company,
        position=position,
        preferences=preferences
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Subscription operations
def get_subscription(db: Session, subscription_id: str):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def get_subscriptions_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).filter(models.Subscription.user_id == user_id).offset(skip).limit(limit).all()

def create_subscription(db: Session, user_id: str, designer_id: str, notification_frequency: str = "daily",
                       auto_purchase: bool = False, max_price: Optional[float] = None):
    db_subscription = models.Subscription(
        user_id=user_id,
        designer_id=designer_id,
        notification_frequency=notification_frequency,
        auto_purchase=auto_purchase,
        max_price=max_price
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

# Voice Command operations
def get_voice_command(db: Session, command_id: str):
    return db.query(models.VoiceCommand).filter(models.VoiceCommand.id == command_id).first()

def get_voice_commands_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.VoiceCommand).filter(models.VoiceCommand.user_id == user_id).offset(skip).limit(limit).all()

def create_voice_command(db: Session, user_id: str, command: str, processed: bool = False, response: Optional[str] = None):
    db_command = models.VoiceCommand(
        user_id=user_id,
        command=command,
        processed=processed,
        response=response
    )
    db.add(db_command)
    db.commit()
    db.refresh(db_command)
    return db_command