
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class FunnelStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"

class StepType(str, enum.Enum):
    LANDING = "landing"
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    PAYMENT = "payment"
    CONDITION = "condition"
    WAIT = "wait"

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    domain = Column(String, unique=True, index=True)
    logo_url = Column(String, nullable=True)
    colors = Column(JSON, nullable=True)  # {"primary": "#...", "secondary": "#..."}
    stripe_account_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship("User", back_populates="tenant")
    funnels = relationship("Funnel", back_populates="tenant")
    leads = relationship("Lead", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant", back_populates="users")

class Funnel(Base):
    __tablename__ = "funnels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    status = Column(String, default=FunnelStatus.DRAFT)
    structure = Column(JSON)  # React Flow JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tenant = relationship("Tenant", back_populates="funnels")
    leads = relationship("Lead", back_populates="funnel")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    funnel_id = Column(Integer, ForeignKey("funnels.id"))
    current_step_id = Column(String, nullable=True)
    score = Column(Float, default=0.0)
    data = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tenant = relationship("Tenant", back_populates="leads")
    funnel = relationship("Funnel", back_populates="leads")
