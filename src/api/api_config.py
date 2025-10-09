"""
API Configuration for GlobalScope MultiFrame 11.0
This file contains the configuration for registering all API routers.
"""
from fastapi import FastAPI
from src.api.routers import (
    system_router, auth_router, chip_router, analytics_router, security_router,
    hash_router, simulation_router, collaboration_router, driver_router,
    voice_router, bci_router, community_router, designer_router, fab_router,
    ai_router, training_router, ip_router, marketplace_router, dao_router,
    iot_router, web3_router, zero_day_router, partner_router, tender_router,
    admin_router, health_router, optimization_router
)
from src.api.cad_api import router as cad_router
from src.api.cad_monitoring_api import router as cad_monitoring_router
from src.api.cad_enhancements import router as cad_enhancements_router
from src.api.cad_ai_optimization_api import router as cad_ai_optimization_router
from src.api.cad_ai_optimization_api_v2 import router as cad_ai_optimization_v2_router
from src.api.ml_training_api import router as ml_training_router

def register_routers(app: FastAPI):
    """Register all API routers with the FastAPI application."""
    # Register all routers
    app.include_router(system_router)
    app.include_router(auth_router)
    app.include_router(chip_router)
    app.include_router(analytics_router)
    app.include_router(security_router)
    app.include_router(hash_router)
    app.include_router(simulation_router)
    app.include_router(collaboration_router)
    app.include_router(driver_router)
    app.include_router(voice_router)
    app.include_router(bci_router)
    app.include_router(community_router)
    app.include_router(designer_router)
    app.include_router(fab_router)
    app.include_router(ai_router)
    app.include_router(training_router)
    app.include_router(ip_router)
    app.include_router(marketplace_router)
    app.include_router(dao_router)
    app.include_router(iot_router)
    app.include_router(web3_router)
    app.include_router(zero_day_router)
    app.include_router(partner_router)
    app.include_router(tender_router)
    app.include_router(admin_router)
    app.include_router(health_router)
    app.include_router(optimization_router)
    app.include_router(cad_router)
    app.include_router(cad_monitoring_router)
    app.include_router(ml_training_router)
    app.include_router(cad_enhancements_router)
    app.include_router(cad_ai_optimization_router)
    app.include_router(cad_ai_optimization_v2_router)
    
    return app