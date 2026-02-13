
import asyncio
from ..base_agent import BaseAgent

class MarketResearcher(BaseAgent):
    def __init__(self, config):
        super().__init__("market_researcher", config)

    async def run(self):
        self.logger.info("Agente Investigador iniciado")
        while True:
            try:
                self.logger.info("Searching strictly for blue ocean trends...")
                # Mock logic for simulation
                trends = ["AI automation for plumbing", "VR for elderly care"]
                
                for trend in trends:
                    await self.remember(f"trend_{trend}", {"name": trend, "score": 0.9})
                    
                self.logger.info(f"Found {len(trends)} blue ocean trends.")
                await asyncio.sleep(60) # Short sleep for demo
            except Exception as e:
                self.logger.error(f"Error en ciclo: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    agent = MarketResearcher({})
    asyncio.run(agent.run())
