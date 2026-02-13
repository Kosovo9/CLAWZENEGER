from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.payment_gateways import MercadoPagoGateway, PayPalGateway
import uuid

router = APIRouter(prefix="/payments", tags=["payments"])

class PaymentInit(BaseModel):
    lead_id: int
    funnel_id: int
    amount: float
    currency: str = "USD"

@router.post("/mercadopago/init")
async def init_mercadopago(data: PaymentInit):
    mp = MercadoPagoGateway()
    items = [{"title": f"Funnel Service {data.funnel_id}", "quantity": 1, "unit_price": data.amount, "currency_id": data.currency}]
    payer = {"email": "test_user@example.com"}
    back = {"success": "http://localhost:3000/success", "pending": "http://localhost:3000/pending", "failure": "http://localhost:3000/failure"}

    pref = mp.create_preference(items, payer, back)
    if not pref: raise HTTPException(status_code=500, detail="MP Error")

    return {"init_point": pref["init_point"], "id": str(uuid.uuid4())}

@router.post("/paypal/init")
async def init_paypal(data: PaymentInit):
    pp = PayPalGateway()
    order = pp.create_order(data.amount, data.currency, "http://localhost:3000/success", "http://localhost:3000/cancel")
    if not order: raise HTTPException(status_code=500, detail="PayPal Error")

    approve_link = next((l["href"] for l in order["links"] if l["rel"] == "approve"), None)
    return {"approve_url": approve_link, "id": str(uuid.uuid4())}

@router.post("/transfer/init")
async def init_transfer(data: PaymentInit):
    return {
        "id": str(uuid.uuid4()),
        "bank_details": {
            "bank": "CLAW BANK",
            "account": "1234567890",
            "clabe": "012345678901234567"
        },
        "instructions": "Transfer manual needed."
    }