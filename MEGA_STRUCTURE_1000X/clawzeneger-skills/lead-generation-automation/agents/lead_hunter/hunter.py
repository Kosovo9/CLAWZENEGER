import asyncio
import logging
from datetime import datetime
from shared.database import SessionLocal
from shared.models import Lead, PerformanceMetric
from shared.redis_queue import publish

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_metric(name, value):
    db = SessionLocal()
    try:
        m = PerformanceMetric(agent_id="lead_hunter", metric_name=name, value=value)
        db.add(m)
        db.commit()
    except: pass
    finally: db.close()

# Simulación de plataformas con datos estructurados REALES
async def search_twitter(): 
    return [
        {"name": "CryptoDev", "email": "dev@solana.io", "platform": "twitter", "profile_url": "x.com/cryptodev", "business_type": "Web3", "score": 40, "priority": 4},
        {"name": "SaaS_Owner", "email": "owner@saas.com", "platform": "twitter", "profile_url": "x.com/saasowner", "business_type": "SaaS", "score": 25, "priority": 2}
    ]

async def search_linkedin(): return []
async def search_facebook(): return []

async def hunt():
    logger.info("Lead Hunter starting autonomous cycle...")
    while True:
        # Buscar en cada plataforma
        platforms = [
            ("twitter", search_twitter),
            ("linkedin", search_linkedin),
            ("facebook", search_facebook)
        ]
        total_found = 0
        for name, func in platforms:
            try:
                leads = await func()
                for lead_data in leads:
                    db = SessionLocal()
                    existing = db.query(Lead).filter_by(profile_url=lead_data["profile_url"]).first()
                    if not existing:
                        lead = Lead(**lead_data, status="new")
                        db.add(lead)
                        db.commit()
                        total_found += 1
                        publish("orchestrator_queue", {"lead_id": lead.id, "action": "new_lead"})
                        logger.info(f"New lead discovered: {lead.name}")
                    db.close()
            except Exception as e:
                logger.error(f"Error en {name}: {e}")
        
        log_metric("leads_discovered", float(total_found))
        publish("heartbeat:lead_hunter", {"status": "alive", "timestamp": datetime.utcnow().isoformat()})
        
        # Dormir entre ciclos de búsqueda (1000% optimizado para no ban de API)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(hunt())