# src/webxr/admin_panel.py
# Панель адміністрування для управління платформою та користувачами

from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from src.lib.utils import get_logger
from src.webxr.holoartem_ar import holo_artem_instance as holo_artem
import aiohttp
from datetime import datetime

class AdminPanel:
    def __init__(self):
        self.logger = get_logger("AdminPanel", logging.INFO)
        self.app = FastAPI()
        self.register_routes()

    async def manage_system(self, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Managing system: {admin_data}")
            action = admin_data.get("action", "status_check")
            if action not in ["status_check", "user_management", "system_restart", "kpi_report"]:
                raise HTTPException(status_code=400, detail="Invalid admin action")
            async with aiohttp.ClientSession() as session:
                async with session.post("http://webxr-service:80/admin", json={
                    "action": action,
                    "timestamp": datetime.utcnow().isoformat()
                }) as resp:
                    if resp.status != 200:
                        raise HTTPException(status_code=resp.status, detail="Admin action failed")
            await holo_artem.notify_ar(
                f"Адмін-дія {action} виконана з любов'ю та інноваціями! 🌌", lang="uk"
            )
            return {"status": "success", "action": action}
        except Exception as e:
            self.logger.error(f"Admin action error: {str(e)}")
            await holo_artem.notify_ar(f"Помилка адмін-дії: {str(e)}", lang="uk")
            return {"error": str(e)}

    def register_routes(self):
        @self.app.post("/admin/manage")
        async def manage_system_endpoint(admin_data: Dict[str, Any]):
            return await self.manage_system(admin_data)