from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Affiliate
from ..core.auth import get_current_user, generate_referral_code
from ..config import settings
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/affiliates", tags=["affiliates"])

class AffiliateResponse(BaseModel):
    id: str
    user_id: str
    referral_code: str
    commission_rate: float
    total_earned: float
    available_balance: float
    pending_balance: float
    paypal_email: Optional[str] = None
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=AffiliateResponse)
async def register_affiliate(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Affiliate).filter(Affiliate.user_id == user_id).first()
    if existing:
        return existing
    
    ref_code = generate_referral_code(user_id)
    affiliate = Affiliate(
        user_id=user_id,
        referral_code=ref_code,
        commission_rate=settings.DEFAULT_COMMISSION_RATE
    )
    db.add(affiliate)
    db.commit()
    db.refresh(affiliate)
    return affiliate

@router.get("/me", response_model=AffiliateResponse)
async def get_me(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    affiliate = db.query(Affiliate).filter(Affiliate.user_id == user_id).first()
    if not affiliate:
        raise HTTPException(status_code=404, detail="No eres un afiliado")
    return affiliate

@router.get("/stats")
async def get_stats(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    affiliate = db.query(Affiliate).filter(Affiliate.user_id == user_id).first()
    if not affiliate:
        raise HTTPException(status_code=404, detail="No eres un afiliado")
    
    return {
        "referrals_count": len(affiliate.referrals),
        "conversions": sum(1 for r in affiliate.referrals if r.status == "converted"),
        "total_earned": affiliate.total_earned,
        "available_balance": affiliate.available_balance,
        "pending_balance": affiliate.pending_balance,
        "referral_link": f"{settings.BASE_URL}/ref/{affiliate.referral_code}"
    }
