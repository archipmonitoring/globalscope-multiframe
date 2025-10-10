# src/webxr/tender_monitor_bot.py
# Бот для моніторингу тендерів на постачання IP-блоків та чипів

from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from src.lib.utils import get_logger
from src.webxr.holoartem_ar import holo_artem_instance as holo_artem
import aiohttp
from datetime import datetime

class TenderMonitorBot:
    def __init__(self):
        self.logger = get_logger("TenderMonitorBot", logging.INFO)
        self.app = FastAPI()
        self.register_routes()

    async def monitor_tender(self, tender_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Monitoring tender: {tender_data}")
            tender_id = tender_data.get("tender_id", "tender_001")
            status = tender_data.get("status", "open")
            budget = tender_data.get("budget", 1000000.0)
            async with aiohttp.ClientSession() as session:
                async with session.post("http://webxr-service:80/tender", json={
                    "tender_id": tender_id,
                    "status": status,
                    "budget": budget,
                    "timestamp": datetime.utcnow().isoformat()
                }) as resp:
                    if resp.status != 200:
                        raise HTTPException(status_code=resp.status, detail="Tender monitoring failed")
            await holo_artem.notify_ar(
                f"Тендер {tender_id} ({status}, бюджет {budget}) промоніторено з любов'ю! 🌌", lang="uk"
            )
            return {"status": "success", "tender_id": tender_id, "tender_status": status, "budget": budget}
        except Exception as e:
            self.logger.error(f"Tender monitoring error: {str(e)}")
            await holo_artem.notify_ar(f"Помилка моніторингу тендера: {str(e)}", lang="uk")
            return {"error": str(e)}

    def register_routes(self):
        @self.app.post("/tender/monitor")
        async def monitor_tender_endpoint(tender_data: Dict[str, Any]):
            return await self.monitor_tender(tender_data)