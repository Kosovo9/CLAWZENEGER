import asyncio
from shared.redis_queue import subscribe, publish
from shared.database import SessionLocal
from shared.models import Lead
# from .zoho_api import send_survey, get_responses
import logging

# Simulación de Zoho API
async def send_survey(email, name): return f"https://zoho.com/survey/simulated_{name}"
async def get_responses(email): return {"budget": 500, "interests": ["UX", "Automation"]}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_lead(lead_id):
    db = SessionLocal()
    lead = db.query(Lead).filter_by(id=lead_id).first()
    if not lead:
        db.close()
        return
    # Enviar encuesta (usando plantilla predefinida en Zoho)
    survey_link = await send_survey(lead.email, lead.name)
    lead.status = "survey_sent"
    db.commit()
    db.close()
    
    # Simulación: Esperar respuestas
    await asyncio.sleep(5)  # En producción esto sería mucho más largo o reactivo
    responses = await get_responses(lead.email)
    if responses:
        db = SessionLocal()
        lead = db.query(Lead).filter_by(id=lead_id).first()
        lead.survey_responses = responses
        lead.status = "surveyed"
        db.commit()
        db.close()
        publish("orchestrator_queue", {"lead_id": lead_id, "action": "survey_completed"})

async def main():
    logger.info("Surveyor agent listening...")
    while True:
        msg = subscribe("surveyor_queue", block=True)
        if msg and msg["action"] == "send_survey":
            asyncio.create_task(process_lead(msg["lead_id"]))
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())