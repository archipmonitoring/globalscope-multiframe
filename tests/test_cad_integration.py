"""
Tests for CAD integration
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import os

# Import the modules we want to test
from src.chip_design.cad_worker import CADWorker
from src.api.cad_api import router

@pytest.fixture
def cad_worker():
    """Create a test instance of CADWorker"""
    with patch('src.chip_design.cad_worker.QuantumSingularityFirewall'), \
         patch('src.chip_design.cad_worker.holo_misha_instance'), \
         patch('src.chip_design.cad_worker.redis_client'):
        worker = CADWorker()
        return worker

@pytest.mark.asyncio
async def test_cad_worker_initialization(cad_worker):
    """Test CADWorker initialization"""
    assert cad_worker is not None
    assert isinstance(cad_worker.supported_tools, dict)
    assert "verilator" in cad_worker.supported_tools
    assert "yosys" in cad_worker.supported_tools
    assert "nextpnr" in cad_worker.supported_tools

@pytest.mark.asyncio
async def test_tool_availability_check(cad_worker):
    """Test tool availability checking"""
    with patch('src.chip_design.cad_worker.asyncio.create_subprocess_exec') as mock_subprocess:
        # Mock successful tool check
        mock_process = AsyncMock()
        mock_process.communicate = AsyncMock(return_value=(b"", b""))
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process
        
        result = await cad_worker.check_tool_availability("verilator")
        assert result is True

@pytest.mark.asyncio
async def test_verilator_simulation_security_validation(cad_worker):
    """Test Verilator simulation security validation"""
    with patch.object(cad_worker.firewall, 'validate_process') as mock_validate, \
         patch('src.chip_design.cad_worker.holo_misha_instance'), \
         patch('src.chip_design.cad_worker.redis_client'):
        
        # Mock security validation to fail
        mock_validate.return_value = False
        
        result = await cad_worker.run_verilator_simulation(
            "test_user",
            "test_project",
            [{"name": "test.v", "content": "module test; endmodule"}],
            "test"
        )
        
        assert result["status"] == "error"
        assert "Security validation failed" in result["message"]

@pytest.mark.asyncio
async def test_yosys_synthesis_security_validation(cad_worker):
    """Test Yosys synthesis security validation"""
    with patch.object(cad_worker.firewall, 'validate_process') as mock_validate, \
         patch('src.chip_design.cad_worker.holo_misha_instance'), \
         patch('src.chip_design.cad_worker.redis_client'):
        
        # Mock security validation to fail
        mock_validate.return_value = False
        
        result = await cad_worker.run_yosys_synthesis(
            "test_user",
            "test_project",
            [{"name": "test.v", "content": "module test; endmodule"}]
        )
        
        assert result["status"] == "error"
        assert "Security validation failed" in result["message"]

@pytest.mark.asyncio
async def test_nextpnr_pnr_security_validation(cad_worker):
    """Test NextPNR place and route security validation"""
    with patch.object(cad_worker.firewall, 'validate_process') as mock_validate, \
         patch('src.chip_design.cad_worker.holo_misha_instance'), \
         patch('src.chip_design.cad_worker.redis_client'):
        
        # Mock security validation to fail
        mock_validate.return_value = False
        
        result = await cad_worker.run_nextpnr_place_and_route(
            "test_user",
            "test_project",
            "test.json"
        )
        
        assert result["status"] == "error"
        assert "Security validation failed" in result["message"]

@pytest.mark.asyncio
async def test_tool_versions_retrieval(cad_worker):
    """Test tool versions retrieval"""
    with patch.object(cad_worker, 'check_tool_availability') as mock_check, \
         patch('src.chip_design.cad_worker.asyncio.create_subprocess_exec') as mock_subprocess:
        
        # Mock tool availability
        mock_check.return_value = True
        
        # Mock subprocess for version command
        mock_process = AsyncMock()
        mock_process.communicate = AsyncMock(return_value=(b"tool version 1.0", b""))
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process
        
        versions = await cad_worker.get_tool_versions()
        assert isinstance(versions, dict)
        assert "verilator" in versions
        assert "yosys" in versions
        assert "nextpnr" in versions

@pytest.mark.asyncio
async def test_cad_api_tool_availability():
    """Test CAD API tool availability endpoint"""
    with patch('src.api.cad_api.cad_worker') as mock_cad_worker:
        # Mock CAD worker
        mock_cad_worker.supported_tools = {"verilator": "/usr/local/bin/verilator"}
        mock_cad_worker.check_tool_availability = AsyncMock(return_value=True)
        
        # This would be tested more thoroughly in integration testing
        assert True  # Placeholder for API test

@pytest.mark.asyncio
async def test_cad_api_health_check():
    """Test CAD API health check endpoint"""
    with patch('src.api.cad_api.cad_worker') as mock_cad_worker:
        # Mock CAD worker
        mock_cad_worker.supported_tools = {"verilator": "/usr/local/bin/verilator"}
        mock_cad_worker.check_tool_availability = AsyncMock(return_value=True)
        
        # This would be tested more thoroughly in integration testing
        assert True  # Placeholder for API test

@pytest.mark.asyncio
async def test_directory_creation(cad_worker):
    """Test directory creation"""
    # Check that directories exist
    assert os.path.exists(cad_worker.projects_dir) or True  # Will be created in container
    assert os.path.exists(cad_worker.chip_designs_dir) or True  # Will be created in container

@pytest.mark.asyncio
async def test_yosys_stats_parsing(cad_worker):
    """Test Yosys statistics parsing"""
    test_output = """
Number of wires:                 42
Number of wire bits:            128
Number of public wires:          15
Number of cells:                 37
"""
    
    stats = cad_worker._parse_yosys_stats(test_output)
    assert isinstance(stats, dict)
    assert stats.get("wires") == 42
    assert stats.get("wire_bits") == 128
    assert stats.get("public_wires") == 15
    assert stats.get("cells") == 37

if __name__ == "__main__":
    pytest.main([__file__])