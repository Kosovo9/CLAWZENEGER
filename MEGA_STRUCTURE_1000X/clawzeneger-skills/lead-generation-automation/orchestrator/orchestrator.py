import asyncio
from shared.redis_queue import subscribe, publish
from shared.database import SessionLocal
from shared.models import Lead, Campaign, Audit, PerformanceMetric

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_metric(agent_id, name, value):
    db = SessionLocal()
    try:
        metric = PerformanceMetric(agent_id=agent_id, metric_name=name, value=value)
        db.add(metric)
        db.commit()
    except Exception as e:
        logger.error(f"Error logging metric: {e}")
    finally:
        db.close()

async def handle_new_lead(lead_id):
    logger.info(f"Handling new lead: {lead_id}")
    log_metric("orchestrator", "new_lead_received", 1.0)
    publish("surveyor_queue", {"action": "send_survey", "lead_id": lead_id})

async def handle_survey_completed(lead_id):
    logger.info(f"Survey completed for lead: {lead_id}")
    db = SessionLocal()
    lead = db.query(Lead).filter_by(id=lead_id).first()
    if lead and lead.survey_responses:
        budget = lead.survey_responses.get("budget", 0)
        if budget >= 100:
            campaign = db.query(Campaign).filter_by(name="default").first()
            if not campaign:
                campaign = Campaign(name="default", offer_a="Auditoría UX", offer_b="Micro-SaaS", offer_c="Landing optimizada")
                db.add(campaign)
                db.commit()
            publish("validator_queue", {"action": "validate", "campaign_id": campaign.id})
        else:
            lead.status = "low_budget"
            db.commit()
    db.close()

async def handle_winner_selected(campaign_id, winner):
    logger.info(f"Winner selected for campaign {campaign_id}: {winner}")
    db = SessionLocal()
    # OPTIMIZATION 1000%: Process top priority leads first
    leads = db.query(Lead).filter(Lead.status == "surveyed").order_by(Lead.priority.desc(), Lead.score.desc()).all()
    for lead in leads:
        publish("auditor_queue", {"action": "start_audit", "lead_id": lead.id})
    log_metric("orchestrator", "batch_audit_triggered", float(len(leads)))
    db.close()

async def handle_audit_ready(lead_id):
    logger.info(f"Audit ready for lead: {lead_id}")
    db = SessionLocal()
    campaign = db.query(Campaign).filter_by(name="default").first()
    if campaign and campaign.winner:
        publish("closer_queue", {"action": "send_proposal", "lead_id": lead_id, "winner": campaign.winner})
    db.close()

async def main():
    logger.info("Orchestrator listening on orchestrator_queue...")
    # Heartbeat task
    async def heartbeat():
        while True:
            publish("heartbeat:orchestrator", {"status": "alive", "timestamp": datetime.utcnow().isoformat()})
            log_metric("orchestrator", "uptime_heartbeat", 1.0)
            await asyncio.sleep(30)

    asyncio.create_task(heartbeat())
    
    while True:
        msg = subscribe("orchestrator_queue", block=True)
        if msg:
            action = msg.get("action")
            start_time = datetime.utcnow()
            if action == "new_lead":
                await handle_new_lead(msg["lead_id"])
            elif action == "survey_completed":
                await handle_survey_completed(msg["lead_id"])
            elif action == "winner_selected":
                await handle_winner_selected(msg["campaign_id"], msg["winner"])
            elif action == "audit_ready":
                await handle_audit_ready(msg["lead_id"])
            
            end_time = datetime.utcnow()
            latency = (end_time - start_time).total_seconds()
            log_metric("orchestrator", "task_latency", latency)
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())