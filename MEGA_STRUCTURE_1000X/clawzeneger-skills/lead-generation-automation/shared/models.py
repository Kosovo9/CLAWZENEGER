from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    platform = Column(String)
    profile_url = Column(String)
    business_type = Column(String)
    pain_points = Column(JSON)
    survey_responses = Column(JSON)
    score = Column(Integer, default=0)
    priority = Column(Integer, default=1)  # 1-5
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'
    id = Column(Integer, primary_key=True)
    agent_id = Column(String)
    metric_name = Column(String)  # latency, cpu, mem
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    offer_a = Column(Text)
    offer_b = Column(Text)
    offer_c = Column(Text)
    winner = Column(String)  # oferta ganadora
    helpfull_test_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Audit(Base):
    __tablename__ = 'audits'
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer)
    maze_study_id = Column(String)
    report_path = Column(String)
    sent_at = Column(DateTime)
    converted = Column(Boolean, default=False)