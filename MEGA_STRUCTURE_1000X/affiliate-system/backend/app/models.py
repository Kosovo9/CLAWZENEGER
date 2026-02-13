from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Affiliate(Base):
    __tablename__ = "affiliates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True, nullable=False)
    referral_code = Column(String, unique=True, nullable=False)
    commission_rate = Column(Float, default=30.0)
    total_earned = Column(Float, default=0)
    available_balance = Column(Float, default=0)
    pending_balance = Column(Float, default=0)
    paypal_email = Column(String)
    bank_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    referrals = relationship("Referral", back_populates="affiliate")
    commissions = relationship("Commission", back_populates="affiliate")
    payouts = relationship("PayoutRequest", back_populates="affiliate")

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    affiliate_id = Column(String, ForeignKey("affiliates.id"))
    lead_id = Column(String)
    referral_url = Column(Text)
    clicked_at = Column(DateTime)
    converted_at = Column(DateTime)
    commission_amount = Column(Float)
    status = Column(String, default="pending") 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    affiliate = relationship("Affiliate", back_populates="referrals")
    commissions = relationship("Commission", back_populates="referral")

class Commission(Base):
    __tablename__ = "commissions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    affiliate_id = Column(String, ForeignKey("affiliates.id"))
    referral_id = Column(String, ForeignKey("referrals.id"))
    transaction_id = Column(String)
    amount = Column(Float)
    status = Column(String, default="pending")
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    affiliate = relationship("Affiliate", back_populates="commissions")
    referral = relationship("Referral", back_populates="commissions")

class PayoutRequest(Base):
    __tablename__ = "payout_requests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    affiliate_id = Column(String, ForeignKey("affiliates.id"))
    amount = Column(Float)
    method = Column(String)
    account_details = Column(JSON)
    status = Column(String, default="pending")
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    affiliate = relationship("Affiliate", back_populates="payouts")
