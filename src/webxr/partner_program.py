# src/webxr/partner_program.py
# Програма партнерства для співпраці з фабриками та організаціями

from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from src.lib.utils import get_logger
from src.webxr.holoartem_ar import holo_artem_instance as holo_artem
import aiohttp
from datetime import datetime

class PartnerProgram:
    def __init__(self):
        self.logger = get_logger("PartnerProgram", logging.INFO)
        self.app = FastAPI()
        self.register_routes()

    async def register_partner(self, partner_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Registering partner: {partner_data}")
            partner_id = partner_data.get("partner_id", "partner_001")
            partner_name = partner_data.get("partner_name", "TSMC")
            async with aiohttp.ClientSession() as session:
                async with session.post("http://webxr-service:80/partner", json={
                    "partner_id": partner_id,
                    "partner_name": partner_name,
                    "timestamp": datetime.utcnow().isoformat()
                }) as resp:
                    if resp.status != 200:
                        raise HTTPException(status_code=resp.status, detail="Partner registration failed")
            await holo_artem.notify_ar(
                f"Партнер {partner_name} ({partner_id}) зареєстровано з любов'ю! 🌌", lang="uk"
            )
            return {"status": "success", "partner_id": partner_id, "partner_name": partner_name}
        except Exception as e:
            self.logger.error(f"Partner registration error: {str(e)}")
            await holo_artem.notify_ar(f"Помилка реєстрації партнера: {str(e)}", lang="uk")
            return {"error": str(e)}

    def register_routes(self):
        @self.app.post("/partner/register")
        async def register_partner_endpoint(partner_data: Dict[str, Any]):
            return await self.register_partner(partner_data)