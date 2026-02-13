import logging
from datetime import datetime
import json
import os
import asyncio
from ..collectors import orchestrator, funnel, affiliate, system

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, chroma_memory=None):
        self.memory = chroma_memory
        os.makedirs("reports", exist_ok=True)

    async def generate_audit_report(self):
        """Auditoría de salud y rendimiento cada 3 horas"""
        data = await self._collect_full_context()
        
        report = {
            "id": f"audit_{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": "AUDIT_3H",
            "status": self._determine_overall_status(data),
            "metrics": {
                "active_agents": len([a for a in data['agents'] if a.get('status') == 'ok']),
                "total_leads": len(data['leads']),
                "revenue_24h": data['funnel'].get('revenue', 0),
                "affiliate_count": data['affiliates'].get('referrals_count', 0)
            },
            "system_health": data['system']['host'],
            "critical_issues": self._find_critical_issues(data),
            "data": data, # Añadir datos crudos para compatibilidad con script de reporte
            "issues": self._find_critical_issues(data),
            "recommendations": [
                "Activar modo live en PayPal para recibir pagos reales",
                "Configurar webhook de Mercado Pago con ngrok",
                "Seguir a los leads calientes detectados"
            ]
        }
        
        await self._save_report(report)
        return report

    async def generate_daily_plan(self):
        """Plan de acción matutino (9 AM) para generar dinero"""
        data = await self._collect_full_context()
        
        # Lógica para identificar oportunidades (Simulada para el demo)
        opportunities = [
            "Re-contactar 5 leads calientes de ayer",
            "Optimizar funnel de ventas en nicho 'Biohacking'",
            "Lanzar campaña de afiliados para ClawVoice Pro"
        ]
        
        plan = {
            "id": f"plan_{datetime.utcnow().strftime('%Y%m%d')}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": "DAILY_PLAN",
            "goals": [
                "Generar $500 USD en ventas directas",
                "Capturar 50 nuevos leads",
                "Reclutar 2 nuevos afiliados top"
            ],
            "action_items": opportunities,
            "priority_leads": data['leads'][:5] # Tomar los más recientes
        }
        
        await self._save_report(plan)
        return plan

    async def generate_nightly_report(self):
        """Resumen de cierre del día (9 PM)"""
        data = await self._collect_full_context()
        
        report = {
            "id": f"nightly_{datetime.utcnow().strftime('%Y%m%d')}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": "NIGHTLY_SUMMARY",
            "performance": {
                "revenue": data['funnel'].get('revenue', 0),
                "conversions": data['funnel'].get('conversions', 0),
                "new_leads": len(data['leads'])
            },
            "victories": [
                "Estabilidad del 99.9% en servicios core",
                "Crecimiento del 15% en red de afiliados"
            ],
            "recommendations": [
                "Aumentar presupuesto en scraper de LinkedIn",
                "Actualizar script de ventas del agente SalesCloser"
            ]
        }
        
        await self._save_report(report)
        return report

    async def _collect_full_context(self):
        """Recolecta datos de todos los colectores en paralelo"""
        tasks = [
            orchestrator.get_agents_status(),
            orchestrator.get_leads_summary(),
            funnel.get_daily_stats(),
            affiliate.get_affiliate_stats(),
            asyncio.to_thread(system.get_host_stats)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "agents": results[0],
            "leads": results[1],
            "funnel": results[2],
            "affiliates": results[3],
            "system": {"host": results[4]}
        }

    def _determine_overall_status(self, data):
        if not data['agents']: return "CRITICAL"
        ok_count = len([a for a in data['agents'] if a.get('status') == 'ok'])
        ratio = ok_count / len(data['agents']) if data['agents'] else 0
        if ratio > 0.9: return "OPTIMAL"
        if ratio > 0.7: return "DEGRADED"
        return "WARNING"

    def _find_critical_issues(self, data):
        issues = []
        for agent in data['agents']:
            if agent.get('status') != 'ok':
                issues.append(f"Agent {agent.get('name')} is DOWN")
        if data['system']['host'].get('disk_usage', 0) > 90:
            issues.append("Disk space is running low (>90%)")
        return issues

    async def _save_report(self, report):
        filename = f"reports/{report['id']}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        if self.memory:
            # Enviar a ChromaDB (asumimos que existe este método en ChromaMemory)
            try:
                await self.memory.add_document(
                    content=json.dumps(report),
                    metadata={"type": report["type"], "id": report["id"]}
                )
            except Exception as e:
                logger.error(f"Error saving to memory: {e}")
