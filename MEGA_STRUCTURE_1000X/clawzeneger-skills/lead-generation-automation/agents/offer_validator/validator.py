import asyncio
from shared.redis_queue import subscribe, publish
from shared.database import SessionLocal
from shared.models import Campaign
# from .helpfull_api import create_test, get_results
import logging

# Simulación de Helpfull API
async def create_test(offers): return "test_12345"
async def get_results(test_id): return [{"option": "Offer A", "score": 85}, {"option": "Offer B", "score": 92}]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def validate_offers(campaign_id):
    db = SessionLocal()
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    if not campaign:
        db.close()
        return
    # Crear test en Helpfull con las 3 ofertas
    test_id = await create_test([
        campaign.offer_a,
        campaign.offer_b,
        campaign.offer_c
    ])
    campaign.helpfull_test_id = test_id
    db.commit()
    # Esperar resultados
    await asyncio.sleep(10) 
    results = await get_results(test_id)
    winner = max(results, key=lambda x: x["score"])["option"]
    campaign.winner = winner
    db.commit()
    db.close()
    publish("orchestrator_queue", {"campaign_id": campaign_id, "action": "winner_selected", "winner": winner})

async def main():
    logger.info("Offer Validator agent listening...")
    while True:
        msg = subscribe("validator_queue", block=True)
        if msg and msg["action"] == "validate":
            asyncio.create_task(validate_offers(msg["campaign_id"]))
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())