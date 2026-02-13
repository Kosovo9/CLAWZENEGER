from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db, SessionLocal
from ..models import Affiliate, Referral, Commission
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/payment-success")
async def payment_success(request: Request):
    """
    Webhook que recibe confirmación de pago del funnel-backend o pasarela.
    Espera JSON: { transaction_id, amount, affiliate_code, lead_id }
    """
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    transaction_id = data.get("transaction_id")
    amount = data.get("amount")
    affiliate_code = data.get("affiliate_code")
    lead_id = data.get("lead_id")

    if not all([transaction_id, amount, affiliate_code]):
        return {"status": "skipped", "reason": "missing data"}

    db = SessionLocal()
    try:
        affiliate = db.query(Affiliate).filter(Affiliate.referral_code == affiliate_code).first()
        if not affiliate:
            return {"status": "skipped", "reason": "invalid affiliate code"}

        # Calcular Comisión (30%)
        commission_amount = float(amount) * (affiliate.commission_rate / 100)

        # Crear registro de referido convertido
        referral = Referral(
            affiliate_id=affiliate.id,
            lead_id=lead_id,
            converted_at=datetime.utcnow(),
            commission_amount=commission_amount,
            status="converted"
        )
        db.add(referral)
        db.flush() # Para obtener el ID

        # Crear comisión
        commission = Commission(
            affiliate_id=affiliate.id,
            referral_id=referral.id,
            transaction_id=str(transaction_id),
            amount=commission_amount,
            status="pending"
        )
        db.add(commission)

        # Actualizar balances
        affiliate.total_earned += commission_amount
        affiliate.pending_balance += commission_amount
        # Nota: available_balance se activa cuando el pago es final (o después de N días)
        
        db.commit()
        logger.info(f"✅ Comisión de ${commission_amount} registrada para {affiliate_code}")
        return {"status": "success", "commission": commission_amount}

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error procesando comisión: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
