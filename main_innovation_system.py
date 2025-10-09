#!/usr/bin/env python3
"""
Main entry point for GlobalScope Innovation Nexus System
"""
import asyncio
import logging
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.lib.utils import get_logger
from src.nexus_orchestrator import nexus_orchestrator

logger = get_logger("MainInnovationSystem")

async def main():
    """Main entry point for the GlobalScope Innovation Nexus System"""
    try:
        print("=" * 60)
        print("🌍 GLOBALSCOPE INNOVATION NEXUS SYSTEM 🌍")
        print("🚀 Creating breakthrough innovations that save lives")
        print("💡 Building a better world through technology")
        print("=" * 60)
        
        # Initialize and start the orchestration system
        print("\n🔄 Initializing GlobalScope systems...")
        init_result = await nexus_orchestrator.initialize_systems()
        
        if init_result["status"] == "success":
            print("✅ All systems initialized successfully!")
            
            # Propose initial breakthrough innovations
            print("\n💡 Proposing breakthrough innovations...")
            
            # Defense innovation (as discussed)
            defense_result = await nexus_orchestrator.propose_human_centered_innovation(
                "defense", 
                "soldier safety and mission success"
            )
            if defense_result["status"] == "success":
                print("✅ Defense innovation proposal submitted!")
            
            # Healthcare innovation
            healthcare_result = await nexus_orchestrator.propose_human_centered_innovation(
                "healthcare", 
                "life-saving medical devices"
            )
            if healthcare_result["status"] == "success":
                print("✅ Healthcare innovation proposal submitted!")
            
            # Environmental innovation
            env_result = await nexus_orchestrator.propose_human_centered_innovation(
                "environment", 
                "climate change solutions"
            )
            if env_result["status"] == "success":
                print("✅ Environmental innovation proposal submitted!")
            
            # Education innovation
            education_result = await nexus_orchestrator.propose_human_centered_innovation(
                "education", 
                "accessible learning for all"
            )
            if education_result["status"] == "success":
                print("✅ Education innovation proposal submitted!")
            
            # Get system status
            status_result = await nexus_orchestrator.get_system_status()
            if status_result["status"] == "success":
                entities = status_result["entities"]
                print(f"\n📊 System Status:")
                print(f"   📋 Monitored Tenders: {entities['monitored_tenders']}")
                print(f"   💡 Innovations: {entities['innovations']}")
                print(f"   📝 Contracts: {entities['contracts']}")
                print(f"   ✅ Verifications: {entities['verifications']}")
            
            print("\n🚀 GlobalScope Innovation Nexus is now operational!")
            print("🎯 Mission: Create breakthrough innovations that save lives")
            print("🌟 Vision: Build a better world through human-centered technology")
            print("\n📡 System is now monitoring for new opportunities...")
            
            # Start the full orchestration system
            await nexus_orchestrator.start_orchestration()
            
        else:
            print(f"❌ System initialization failed: {init_result['message']}")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 System shutdown requested...")
        print("👋 Thank you for using GlobalScope Innovation Nexus!")
        return 0
    except Exception as e:
        logger.error(f"Critical system error: {str(e)}")
        print(f"💥 Critical system error: {str(e)}")
        return 1

if __name__ == "__main__":
    # Run the main async function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)