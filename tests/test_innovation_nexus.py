"""
Test suite for GlobalScope Innovation Nexus System
"""
import sys
import os
import asyncio
import pytest
from unittest.mock import AsyncMock, patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.nexus_orchestrator import nexus_orchestrator
from src.innovation.innovation_nexus import innovation_nexus
from src.tender.quality_assurance_contract import quality_assurance_contract
from src.verification.contract_verification import contract_verification

class TestInnovationNexus:
    """Test suite for GlobalScope Innovation Nexus System"""
    
    @pytest.mark.asyncio
    async def test_system_initialization(self):
        """Test system initialization"""
        result = await nexus_orchestrator.initialize_systems()
        assert result["status"] == "success"
        print("✅ System initialization test passed")
    
    @pytest.mark.asyncio
    async def test_defense_innovation_proposal(self):
        """Test defense innovation proposal"""
        # Propose defense innovation
        result = await nexus_orchestrator.propose_human_centered_innovation(
            "defense", 
            "soldier safety and mission success"
        )
        
        assert result["status"] == "success"
        assert "innovation_id" in result
        
        # Check that innovation was created
        innovation_result = await innovation_nexus.get_innovation_impact(result["innovation_id"])
        assert innovation_result["status"] == "success"
        
        print("✅ Defense innovation proposal test passed")
    
    @pytest.mark.asyncio
    async def test_healthcare_innovation_proposal(self):
        """Test healthcare innovation proposal"""
        # Propose healthcare innovation
        result = await nexus_orchestrator.propose_human_centered_innovation(
            "healthcare", 
            "life-saving medical devices"
        )
        
        assert result["status"] == "success"
        assert "innovation_id" in result
        
        print("✅ Healthcare innovation proposal test passed")
    
    @pytest.mark.asyncio
    async def test_quality_assurance_contract(self):
        """Test quality assurance contract creation"""
        # Create quality commitments
        quality_commitments = {
            "reliability_target": 0.999,
            "performance_specifications": {
                "processing_power": "100 GOPS",
                "power_consumption": "< 5W"
            },
            "testing_procedures": ["design_verification", "performance_testing"],
            "warranty_period_months": 24
        }
        
        # Submit tender proposal
        proposal_data = {
            "is_chip_tender": True,
            "quality_commitments": quality_commitments,
            "delivery_schedule": {"phase_1": "3 months"}
        }
        
        result = await quality_assurance_contract.submit_tender_proposal(
            "test_tender_001",
            "test_company",
            proposal_data
        )
        
        assert result["status"] == "success"
        assert "contract_id" in result
        
        # Verify contract quality
        verify_result = await quality_assurance_contract.verify_contract_quality(result["contract_id"])
        assert verify_result["status"] == "success"
        
        print("✅ Quality assurance contract test passed")
    
    @pytest.mark.asyncio
    async def test_contract_verification(self):
        """Test contract verification system"""
        # Create verification template
        template_result = await contract_verification.create_chip_verification_template()
        assert template_result["status"] == "success"
        
        # Create mock deliverable data
        deliverable_data = {
            "type": "chips",
            "items": [
                {
                    "id": "chip_001",
                    "specifications": "High-performance defense chip"
                }
            ]
        }
        
        # Initiate verification
        verify_result = await contract_verification.initiate_contract_verification(
            "test_contract_001",
            deliverable_data
        )
        
        assert verify_result["status"] == "success"
        assert "verification_id" in verify_result
        
        print("✅ Contract verification test passed")
    
    @pytest.mark.asyncio
    async def test_innovation_evaluation(self):
        """Test innovation evaluation process"""
        # Create mock innovation
        innovation_data = {
            "title": "Test Breakthrough Innovation",
            "description": "Revolutionary technology for societal benefit",
            "category": "scientific",
            "potential_impact": "Transform scientific research",
            "technical_approach": "Groundbreaking methodology",
            "timeline_months": 12,
            "ethical_compliance": True,
            "human_centered": True
        }
        
        # Propose innovation
        propose_result = await innovation_nexus.propose_innovation(
            "test_innovator",
            innovation_data
        )
        
        assert propose_result["status"] == "success"
        
        # Evaluate innovation
        evaluate_result = await innovation_nexus.evaluate_innovation(
            propose_result["innovation_id"],
            ["expert_1", "expert_2"]
        )
        
        assert evaluate_result["status"] == "success"
        assert "evaluation_results" in evaluate_result
        
        print("✅ Innovation evaluation test passed")
    
    @pytest.mark.asyncio
    async def test_impact_tracking(self):
        """Test innovation impact tracking"""
        # Create mock innovation
        innovation_data = {
            "title": "Impact Tracking Test",
            "description": "Innovation for impact measurement",
            "category": "environment",
            "potential_impact": "Environmental benefit",
            "technical_approach": "Sustainable technology",
            "timeline_months": 6
        }
        
        # Propose innovation
        propose_result = await innovation_nexus.propose_innovation(
            "test_impact_tracker",
            innovation_data
        )
        
        assert propose_result["status"] == "success"
        
        # Create impact tracking
        impact_result = await innovation_nexus.create_impact_tracking(
            propose_result["innovation_id"]
        )
        
        assert impact_result["status"] == "success"
        
        # Report milestone
        milestone_data = {
            "description": "First milestone achieved",
            "technical_achievement": "Proof of concept completed",
            "impact_evidence": "Initial testing successful",
            "verified": True,
            "metrics_update": {
                "people_helped": 100,
                "environmental_benefit": 0.5
            }
        }
        
        milestone_result = await innovation_nexus.report_milestone(
            propose_result["innovation_id"],
            milestone_data
        )
        
        assert milestone_result["status"] == "success"
        
        # Get impact metrics
        final_impact = await innovation_nexus.get_innovation_impact(
            propose_result["innovation_id"]
        )
        
        assert final_impact["status"] == "success"
        assert final_impact["total_milestones"] == 1
        
        print("✅ Impact tracking test passed")
    
    @pytest.mark.asyncio
    async def test_system_status(self):
        """Test system status reporting"""
        status_result = await nexus_orchestrator.get_system_status()
        
        assert status_result["status"] == "success"
        assert "entities" in status_result
        assert "system_status" in status_result
        
        print("✅ System status test passed")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])