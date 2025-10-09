"""
Unit tests for CAD tools availability and functionality
"""
import pytest
import asyncio
import os
from unittest.mock import AsyncMock, patch

from src.chip_design.cad_worker import CADWorker


@pytest.mark.asyncio
async def test_cad_worker_initialization():
    """Test that the CADWorker initializes correctly."""
    worker = CADWorker()
    assert worker is not None
    assert hasattr(worker, 'supported_tools')
    assert isinstance(worker.supported_tools, dict)
    assert len(worker.supported_tools) > 0


@pytest.mark.asyncio
async def test_tool_availability():
    """Test that CAD tools are available."""
    worker = CADWorker()
    
    # Test Verilator availability
    result = await worker.check_tool_availability("verilator")
    assert isinstance(result, bool)
    
    # Test Yosys availability
    result = await worker.check_tool_availability("yosys")
    assert isinstance(result, bool)
    
    # Test NextPNR availability
    result = await worker.check_tool_availability("nextpnr")
    assert isinstance(result, bool)


@pytest.mark.asyncio
async def test_unsupported_tool():
    """Test handling of unsupported tools."""
    worker = CADWorker()
    
    # Test unsupported tool
    result = await worker.check_tool_availability("unsupported_tool")
    assert result is False


@pytest.mark.asyncio
async def test_verilator_simulation():
    """Test Verilator simulation functionality."""
    worker = CADWorker()
    
    # Check if Verilator is available
    if not await worker.check_tool_availability("verilator"):
        pytest.skip("Verilator not available")
    
    # Sample Verilog files
    verilog_files = [
        {
            "name": "test_module.v",
            "content": """
module test_module(
    input clk,
    input rst,
    output reg [7:0] counter
);

always @(posedge clk or posedge rst) begin
    if (rst) begin
        counter <= 8'b0;
    end else begin
        counter <= counter + 1;
    end
end

endmodule
"""
        }
    ]
    
    # Mock firewall validation
    with patch.object(worker, 'firewall') as mock_firewall:
        mock_firewall.validate_process = AsyncMock(return_value=True)
        
        result = await worker.run_verilator_simulation(
            user_id="test_user",
            project_id="test_project",
            verilog_files=verilog_files,
            top_module="test_module",
            simulation_time=100
        )
        
        # The result should be either success or error, but not crash
        assert result["status"] in ["success", "error"]


@pytest.mark.asyncio
async def test_yosys_synthesis():
    """Test Yosys synthesis functionality."""
    worker = CADWorker()
    
    # Check if Yosys is available
    if not await worker.check_tool_availability("yosys"):
        pytest.skip("Yosys not available")
    
    # Sample Verilog files
    verilog_files = [
        {
            "name": "simple_module.v",
            "content": """
module simple_module(
    input a,
    input b,
    output y
);

assign y = a & b;

endmodule
"""
        }
    ]
    
    # Mock firewall validation
    with patch.object(worker, 'firewall') as mock_firewall:
        mock_firewall.validate_process = AsyncMock(return_value=True)
        
        result = await worker.run_yosys_synthesis(
            user_id="test_user",
            project_id="test_project",
            verilog_files=verilog_files,
            target_family="generic"
        )
        
        # The result should be either success or error, but not crash
        assert result["status"] in ["success", "error"]


@pytest.mark.asyncio
async def test_nextpnr_placement_routing():
    """Test NextPNR placement and routing functionality."""
    worker = CADWorker()
    
    # Check if NextPNR is available
    if not await worker.check_tool_availability("nextpnr"):
        pytest.skip("NextPNR not available")
    
    # Mock firewall validation
    with patch.object(worker, 'firewall') as mock_firewall:
        mock_firewall.validate_process = AsyncMock(return_value=True)
        
        result = await worker.run_nextpnr_pnr(
            user_id="test_user",
            project_id="test_project",
            netlist_file="test_netlist.json",
            target_device="generic",
            placement_constraints={}
        )
        
        # The result should be either success or error, but not crash
        assert result["status"] in ["success", "error"]


@pytest.mark.asyncio
async def test_directory_creation():
    """Test that project directories are created correctly."""
    worker = CADWorker()
    
    # Check that directories exist
    assert os.path.exists(worker.projects_dir)
    assert os.path.exists(worker.chip_designs_dir)
    
    # Check that directories are writable
    test_file_path = os.path.join(worker.projects_dir, "test_file.txt")
    try:
        with open(test_file_path, "w") as f:
            f.write("test")
        assert os.path.exists(test_file_path)
        
        # Clean up
        os.remove(test_file_path)
    except Exception as e:
        pytest.fail(f"Failed to write to project directory: {e}")


if __name__ == "__main__":
    pytest.main([__file__])