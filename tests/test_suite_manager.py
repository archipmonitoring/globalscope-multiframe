# tests/test_suite_manager.py
# Тести для перевірки KPI та масштабування до 150k користувачів

import pytest
import json
from src.ai.test_suite_manager import TestSuiteManager
from src.webxr.marketplace_brigadier import MarketplaceBrigadier
from src.ai.ai_design_automation import AIDesignAutomation
from src.webxr.holoartem_ar import HoloMishaAR
from src.webxr.bci_interface import BCIInterface
from src.webxr.voice_chat_engine import VoiceChatEngine
from src.fab.iot_integration import IoTIntegration
from src.analytics.chip_analytics import ChipAnalytics
from src.fab.fab_analytics import FabAnalytics
from src.impact.impact_analyzer import ImpactAnalyzer
from src.lib.utils import get_redis_client
import asyncio

@pytest.mark.asyncio
async def test_run_tests():
    tester = TestSuiteManager()
    test_data = {"test_id": "test_001", "module": "marketplace_brigadier"}
    result = await tester.run_tests(test_data)
    assert result["status"] == "success"
    assert result["results"]["passed"] == True

@pytest.mark.asyncio
async def test_ai_design_automation():
    ai_design = AIDesignAutomation()
    design_data = {
        "complexity": 1.0,
        "size": 100.0,
        "power_usage": 0.0035,
        "co2_impact": 0.20,
        "temperature": 25.0,
        "yield_rate": 0.99,
        "frequency": 3.5,
        "cores": 8
    }
    result = await ai_design.optimize_design(design_data)
    assert result["status"] == "success"
    assert result["efficiency"] > 0.98
    assert result["design_id"] == "chip_001"

@pytest.mark.asyncio
async def test_holoartem_ar():
    holoartem = HoloMishaAR()
    await holoartem.notify_ar("Test notification")
    chip_data = {"chip_id": "chip_001", "scale": "0.5 0.5 0.5"}
    result = await holoartem.visualize_chip(chip_data)
    assert result["status"] == "success"
    assert result["chip_id"] == "chip_001"

@pytest.mark.asyncio
async def test_bci_interface():
    bci = BCIInterface()
    bci_data = {"neural_signal": [0.7] * 1024}
    result = await bci.process_bci_command("user_1", bci_data)
    assert result["status"] == "success"
    assert result["bci_output"]["action"] == "design_update"
    assert result["bci_output"]["value"] > 0.6

@pytest.mark.asyncio
async def test_voice_chat_engine():
    voice = VoiceChatEngine()
    command = {"transcript": "створити nft", "lang": "uk"}
    result = await voice.process_voice_command("user_1", command)
    assert result["status"] == "success"
    assert result["voice_output"]["action"] == "create_nft"

@pytest.mark.asyncio
async def test_iot_integration():
    iot = IoTIntegration()
    iot_data = {
        "fab_name": "TSMC",
        "protocol": "MQTT",
        "production_rate": 80e15,
        "defect_rate": 0.0,
        "power_usage": 0.0035,
        "temperature_stability": 0.99,
        "yield_variability": 0.01
    }
    result = await iot.connect_iot(iot_data)
    assert result["status"] == "success"
    assert result["fab_name"] == "TSMC"
    assert result["metrics"]["defect_rate"] == 0.0
    assert result["metrics"]["power_usage"] <= 0.0035

@pytest.mark.asyncio
async def test_chip_analytics():
    analytics = ChipAnalytics()
    chip_data = {
        "chip_id": "chip_001",
        "defect_rate": 0.0,
        "power_usage": 0.0035,
        "co2_impact": 0.20,
        "yield_rate": 0.99,
        "motivation_score": 0.95,
        "productivity_increase": 4.0,
        "investment_cost": 1.0
    }
    result = await analytics.analyze_metrics(chip_data)
    assert result["status"] == "success"
    assert result["metrics"]["defect_rate"] == 0.0
    assert result["metrics"]["power_usage"] <= 0.0035
    assert result["metrics"]["roi"] >= 400.0

@pytest.mark.asyncio
async def test_fab_analytics():
    fab_analytics = FabAnalytics()
    fab_data = {
        "fab_name": "TSMC",
        "production_rate": 80e15,
        "defect_rate": 0.0,
        "power_usage": 0.0035,
        "co2_impact": 0.20,
        "co2_reduction": 0.80,
        "total_production": 1000,
        "productivity_increase": 4.0,
        "investment_cost": 1.0
    }
    result = await fab_analytics.analyze_fab_metrics(fab_data)
    assert result["status"] == "success"
    assert result["metrics"]["defect_rate"] == 0.0
    assert result["metrics"]["power_usage"] <= 0.0035
    assert result["metrics"]["co2_saved_tons"] >= 800
    assert result["metrics"]["roi"] >= 400.0

@pytest.mark.asyncio
async def test_impact_analyzer():
    impact_analyzer = ImpactAnalyzer()
    impact_data = {
        "productivity_increase": 4.0,
        "co2_reduction": 0.80,
        "motivation_score": 0.95,
        "total_production": 1000,
        "investment_cost": 1.0
    }
    result = await impact_analyzer.analyze_impact(impact_data)
    assert result["status"] == "success"
    assert result["impact_metrics"]["roi"] >= 400.0
    assert result["impact_metrics"]["co2_saved_tons"] >= 800
    assert result["impact_metrics"]["motivation_score"] >= 0.95

@pytest.mark.asyncio
async def test_scale_interfaces():
    brigadier = MarketplaceBrigadier()
    redis_client = get_redis_client()
    tasks = []
    for i in range(150000):  # Simulating 150k users
        nft_data = {
            "price": 1.0,
            "rtl_code": f"module chip_{i}(input clk, output reg out); always @(posedge clk) out <= 1; endmodule",
            "name": f"Test Chip {i}",
            "description": "Test NFT",
            "protocol": "opensea"
        }
        tasks.append(brigadier.create_nft_offer(f"chip_{i}", f"user_{i}", nft_data, priority=1))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    successes = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "success")
    assert successes >= 149500  # Allow 0.33% failure
    await holo_artem.notify_ar(
        f"Масштабування до 150k користувачів виконано з любов'ю! 🌌", lang="uk"
    )

def test_api_endpoints():
    client = TestClient(TestSuiteManager().app)
    response = client.post("/tests/run", json={"test_id": "test_001", "module": "marketplace_brigadier"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"