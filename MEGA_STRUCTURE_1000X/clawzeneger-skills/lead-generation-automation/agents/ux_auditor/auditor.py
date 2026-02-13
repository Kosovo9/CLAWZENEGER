import asyncio
from shared.redis_queue import subscribe, publish
from shared.database import SessionLocal
from shared.models import Lead, Audit
# from .maze_api import create_study, get_report
import logging

# Simulación de Maze API
async def create_study(biz_type, pain_points): return "study_999"
async def get_report(study_id): return f"https://maze.co/report/{study_id}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def conduct_audit(lead_id):
    db = SessionLocal()
    lead = db.query(Lead).filter_by(id=lead_id).first()
    if not lead:
        db.close()
        return
    # Crear estudio en Maze
    study_id = await create_study(lead.business_type, lead.pain_points)
    # Esperar resultados
    await asyncio.sleep(15) 
    report_url = await get_report(study_id)
    audit = Audit(lead_id=lead_id, maze_study_id=study_id, report_path=report_url)
    db.add(audit)
    lead.status = "audited"
    db.commit()
    db.close()
    publish("orchestrator_queue", {"lead_id": lead_id, "action": "audit_ready"})

async def main():
    logger.info("UX Auditor agent listening...")
    while True:
        msg = subscribe("auditor_queue", block=True)
        if msg and msg["action"] == "start_audit":
            asyncio.create_task(conduct_audit(msg["lead_id"]))
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())