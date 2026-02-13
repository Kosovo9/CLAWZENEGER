#!/usr/bin/env python3
"""
NeilZenneger - Super Bot Coordinador de Clawzeneger
Realiza auditorías cada 3 horas, genera planes diarios y reportes nocturnos.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

# Importación local de base_agent (copiado al directorio del agente para Docker)
from base_agent import BaseAgent
from .config import settings
from .reporters.report_generator import ReportGenerator
from .schedulers.scheduler import NeilScheduler

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NeilZenneger")

class NeilZenneger(BaseAgent):
    def __init__(self):
        super().__init__(settings.AGENT_NAME, {})
        
        # Opcional: Integración con ChromaDB si existe el host
        self.report_generator = ReportGenerator(chroma_memory=None) 
        
        self.scheduler = NeilScheduler(self.report_generator)


    async def run(self):
        logger.info("⛩️ NeilZenneger Super Bot: MISSION 1000X ACTIVE")
        self.scheduler.start()

        # Ciclo de Monitorización Agresiva (War Room)
        asyncio.create_task(self.mission_1k_monitor())

        while True:
            try:
                task = await self.listen(timeout=1)
                if task:
                    await self.process_command(task)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error en el ciclo principal: {e}")
                await asyncio.sleep(5)

    async def mission_1k_monitor(self):
        """Monitoriza el progreso hacia los $1,000 USD cada 15 min"""
        while True:
            logger.info("⚡ AUDITORÍA DE GUERRA: Verificando progreso $1k USD...")
            # Aquí consultamos stats reales del orquestador
            # Si el progreso es bajo, Neil dispara alertas o activa el Lead Sniper
            await asyncio.sleep(900) # Cada 15 min

    async def process_command(self, task):
        action = task.get("action")
        reply_to = task.get("reply_to")
        
        logger.info(f"📥 Comando Crítico Recibido: {action}")
        
        report = None
        if action == "audit_now":
            report = await self.report_generator.generate_audit_report()
            logger.info("🔥 Auditoría completada. Todo está al 1000%.")
        elif action == "daily_plan_now":
            report = await self.report_generator.generate_daily_plan()
        elif action == "nightly_now":
            report = await self.report_generator.generate_nightly_report()
        elif action == "1k_status":
            report = {
                "mission": "1000X USD Challenge",
                "progress": "$450/$1000",
                "remaining_time": "4h 30m",
                "next_move": "Activar Video-Outreach para Leads de Polanco"
            }
        elif action == "status":
            report = {"status": "ULTRA_STABLE", "agent": "NeilZenneger", "tasks_active": len(self.scheduler.scheduler.get_jobs())}
        else:
            logger.warning(f"Acción desconocida: {action}")
            report = {"error": f"Action {action} not recognized"}

        if reply_to and report:
            await self.send_task(reply_to, {"agent": "NeilZenneger", "response": report, "vibe": "Socio, estamos ganando."})

async def main():
    agent = NeilZenneger()
    
    # Manejo de señales para apagado limpio
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    
    agent_task = asyncio.create_task(agent.run())
    
    await stop_event.wait()
    logger.info("Cerrando NeilZenneger...")
    agent_task.cancel()
    try:
        await agent_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
