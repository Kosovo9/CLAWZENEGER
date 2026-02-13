
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..database import get_db
from ..models import Funnel, Tenant
from pydantic import BaseModel

router = APIRouter()

class FunnelCreate(BaseModel):
    name: str
    structure: Any = {}

class FunnelResponse(BaseModel):
    id: int
    name: str
    status: str
    structure: Any
    tenant_id: int

    class Config:
        from_attributes = True

@router.post("/", response_model=FunnelResponse)
def create_funnel(funnel: FunnelCreate, tenant_id: int = 1, db: Session = Depends(get_db)):
    # Check if tenant exists
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        # Auto-create demo tenant if not exists (for ease of use)
        tenant = Tenant(name="Demo Tenant", domain="demo.clawzeneger.local")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        tenant_id = tenant.id
        
    db_funnel = Funnel(name=funnel.name, structure=funnel.structure, tenant_id=tenant_id)
    db.add(db_funnel)
    db.commit()
    db.refresh(db_funnel)
    return db_funnel

@router.get("/", response_model=List[FunnelResponse])
def read_funnels(skip: int = 0, limit: int = 100, tenant_id: int = 1, db: Session = Depends(get_db)):
    funnels = db.query(Funnel).filter(Funnel.tenant_id == tenant_id).offset(skip).limit(limit).all()
    return funnels

@router.get("/{funnel_id}", response_model=FunnelResponse)
def read_funnel(funnel_id: int, db: Session = Depends(get_db)):
    funnel = db.query(Funnel).filter(Funnel.id == funnel_id).first()
    if funnel is None:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return funnel
