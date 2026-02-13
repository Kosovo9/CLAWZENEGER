import asyncio
from shared.redis_queue import subscribe
from shared.database import SessionLocal
from shared.models import Lead, Campaign, Audit
# from .email_sender import send_proposal
# from .whatsapp_sender import send_whatsapp
import logging

# Simulación de Envío
async def send_proposal(email, proposal): logger.info(f"EMAIL SENT TO {email}: {proposal}")
async def send_whatsapp(phone, proposal): logger.info(f"WHATSAPP SENT TO {phone}: {proposal}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def close_lead(lead_id, winner_offer):
    db = SessionLocal()
    lead = db.query(Lead).filter_by(id=lead_id).first()
    audit = db.query(Audit).filter_by(lead_id=lead_id).first()
    if not lead or not audit:
        db.close()
        return
    # Preparar propuesta personalizada
    proposal = f"Hola {lead.name}, según nuestro análisis y la auditoría UX (ver {audit.report_path}), te recomiendo {winner_offer}. ¿Te gustaría agendar una llamada para implementarlo?"
    # Enviar por email y WhatsApp
    await send_proposal(lead.email, proposal)
    if lead.phone:
        await send_whatsapp(lead.phone, proposal)
    lead.status = "proposal_sent"
    db.commit()
    db.close()

async def main():
    logger.info("Sales Closer agent listening...")
    while True:
        msg = subscribe("closer_queue", block=True)
        if msg and msg["action"] == "send_proposal":
            asyncio.create_task(close_lead(msg["lead_id"], msg["winner"]))
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())