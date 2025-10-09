"""
CAD Worker for GlobalScope MultiFrame 11.0
This module provides integration with CAD tools: Verilator, Yosys, NextPNR
"""

import asyncio
import subprocess
import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.lib.utils import get_logger
from src.lib.redis_client import redis_client
from src.security.quantum_singularity_firewall import QuantumSingularityFirewall
from src.webxr.holomisha_ar import holo_misha_instance

logger = get_logger("CADWorker")

class CADWorker:
    """Worker for CAD tool integration"""
    
    def __init__(self):
        self.firewall = QuantumSingularityFirewall()
        self.supported_tools = {
            "verilator": "/usr/local/bin/verilator",
            "yosys": "/usr/local/bin/yosys",
            "nextpnr": "/usr/local/bin/nextpnr-generic",
            "iverilog": "/usr/bin/iverilog",
            "vvp": "/usr/bin/vvp"
        }
        self.projects_dir = "/app/projects"
        self.chip_designs_dir = "/app/chip_designs"
        
        # Create directories if they don't exist
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.chip_designs_dir, exist_ok=True)
        
        logger.info("CADWorker initialized with tools: %s", list(self.supported_tools.keys()))
    
    async def check_tool_availability(self, tool_name: str) -> bool:
        """Check if a CAD tool is available"""
        if tool_name not in self.supported_tools:
            logger.error(f"Unsupported tool: {tool_name}")
            return False
            
        tool_path = self.supported_tools[tool_name]
        try:
            # Check if tool exists and is executable
            result = await asyncio.create_subprocess_exec(
                "which", tool_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error checking tool {tool_name}: {e}")
            return False
    
    async def run_verilator_simulation(self, user_id: str, project_id: str, verilog_files: list, 
                                     top_module: str, simulation_time: int = 1000) -> Dict[str, Any]:
        """Run Verilator simulation"""
        try:
            # Validate input with firewall
            process_data = {
                "type": "verilator_simulation",
                "user_id": user_id,
                "project_id": project_id,
                "files": verilog_files,
                "top_module": top_module
            }
            
            is_safe = await self.firewall.validate_process(f"verilator_{project_id}", process_data)
            if not is_safe:
                return {"status": "error", "message": "Security validation failed"}
            
            # Create project directory
            project_path = os.path.join(self.projects_dir, project_id)
            os.makedirs(project_path, exist_ok=True)
            
            # Copy Verilog files to project directory
            for file_info in verilog_files:
                file_path = os.path.join(project_path, file_info["name"])
                with open(file_path, "w") as f:
                    f.write(file_info["content"])
            
            # Run Verilator
            cmd = [
                "verilator",
                "--cc",  # C++ output
                "--exe",  # Build executable
                "--build",  # Build automatically
                "--trace",  # Enable tracing
                f"--top-module", top_module,
                f"--Mdir", f"{project_path}/obj_dir"
            ] + [f"{project_path}/{file_info['name']}" for file_info in verilog_files]
            
            logger.info(f"Running Verilator: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=project_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # Run the simulation
                sim_cmd = [f"{project_path}/obj_dir/V{top_module}", f"+verilator+rand+reset+0"]
                
                sim_process = await asyncio.create_subprocess_exec(
                    *sim_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=project_path
                )
                
                sim_stdout, sim_stderr = await sim_process.communicate()
                
                result = {
                    "status": "success",
                    "project_id": project_id,
                    "simulation_output": sim_stdout.decode(),
                    "simulation_errors": sim_stderr.decode(),
                    "trace_file": f"{project_path}/obj_dir/V{top_module}.vcd" if os.path.exists(f"{project_path}/obj_dir/V{top_module}.vcd") else None
                }
                
                # Store result in Redis
                await redis_client.set_json(f"cad_result:verilator:{project_id}", result)
                
                await holo_misha_instance.notify_ar(
                    f"Verilator simulation completed for project {project_id} by {user_id} - HoloMisha programs the universe!", 
                    "uk"
                )
                
                return result
            else:
                error_msg = stderr.decode()
                logger.error(f"Verilator failed: {error_msg}")
                
                await holo_misha_instance.notify_ar(
                    f"Verilator simulation failed for project {project_id} by {user_id}: {error_msg} - HoloMisha programs the universe!", 
                    "uk"
                )
                
                return {
                    "status": "error",
                    "message": "Verilator compilation failed",
                    "error_details": error_msg
                }
                
        except Exception as e:
            logger.error(f"Error in Verilator simulation: {e}")
            
            await holo_misha_instance.notify_ar(
                f"Verilator simulation error for project {project_id} by {user_id}: {str(e)} - HoloMisha programs the universe!", 
                "uk"
            )
            
            return {
                "status": "error",
                "message": f"Verilator simulation error: {str(e)}"
            }
    
    async def run_yosys_synthesis(self, user_id: str, project_id: str, verilog_files: list,
                                target_family: str = "generic") -> Dict[str, Any]:
        """Run Yosys synthesis"""
        try:
            # Validate input with firewall
            process_data = {
                "type": "yosys_synthesis",
                "user_id": user_id,
                "project_id": project_id,
                "files": verilog_files,
                "target_family": target_family
            }
            
            is_safe = await self.firewall.validate_process(f"yosys_{project_id}", process_data)
            if not is_safe:
                return {"status": "error", "message": "Security validation failed"}
            
            # Create project directory
            project_path = os.path.join(self.projects_dir, project_id)
            os.makedirs(project_path, exist_ok=True)
            
            # Create Yosys script
            yosys_script = f"""
read_verilog {" ".join([f'"{project_path}/{file_info["name"]}"' for file_info in verilog_files])}
hierarchy -check
proc
opt
fsm
opt
techmap
opt
abc -liberty /usr/local/share/yosys/cmos_cells.lib
clean
write_verilog {project_path}/synthesized_{project_id}.v
stat
"""
            
            script_path = os.path.join(project_path, "synthesis.ys")
            with open(script_path, "w") as f:
                f.write(yosys_script)
            
            # Copy Verilog files to project directory
            for file_info in verilog_files:
                file_path = os.path.join(project_path, file_info["name"])
                with open(file_path, "w") as f:
                    f.write(file_info["content"])
            
            # Run Yosys
            cmd = ["yosys", "-s", script_path]
            
            logger.info(f"Running Yosys: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=project_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # Read synthesized output
                synthesized_file = f"{project_path}/synthesized_{project_id}.v"
                synthesized_content = ""
                if os.path.exists(synthesized_file):
                    with open(synthesized_file, "r") as f:
                        synthesized_content = f.read()
                
                result = {
                    "status": "success",
                    "project_id": project_id,
                    "synthesis_output": stdout.decode(),
                    "synthesis_errors": stderr.decode(),
                    "synthesized_verilog": synthesized_content,
                    "statistics": self._parse_yosys_stats(stdout.decode())
                }
                
                # Store result in Redis
                await redis_client.set_json(f"cad_result:yosys:{project_id}", result)
                
                await holo_misha_instance.notify_ar(
                    f"Yosys synthesis completed for project {project_id} by {user_id} - HoloMisha programs the universe!", 
                    "uk"
                )
                
                return result
            else:
                error_msg = stderr.decode()
                logger.error(f"Yosys failed: {error_msg}")
                
                await holo_misha_instance.notify_ar(
                    f"Yosys synthesis failed for project {project_id} by {user_id}: {error_msg} - HoloMisha programs the universe!", 
                    "uk"
                )
                
                return {
                    "status": "error",
                    "message": "Yosys synthesis failed",
                    "error_details": error_msg
                }
                
        except Exception as e:
            logger.error(f"Error in Yosys synthesis: {e}")
            
            await holo_misha_instance.notify_ar(
                f"Yosys synthesis error for project {project_id} by {user_id}: {str(e)} - HoloMisha programs the universe!", 
                "uk"
            )
            
            return {
                "status": "error",
                "message": f"Yosys synthesis error: {str(e)}"
            }
    
    def _parse_yosys_stats(self, output: str) -> Dict[str, Any]:
        """Parse Yosys statistics output"""
        stats = {}
        lines = output.split('\n')
        
        for line in lines:
            if "Number of wires:" in line:
                stats["wires"] = int(line.split(":")[1].strip())
            elif "Number of wire bits:" in line:
                stats["wire_bits"] = int(line.split(":")[1].strip())
            elif "Number of public wires:" in line:
                stats["public_wires"] = int(line.split(":")[1].strip())
            elif "Number of cells:" in line:
                stats["cells"] = int(line.split(":")[1].strip())
        
        return stats
    
    async def run_nextpnr_place_and_route(self, user_id: str, project_id: str, 
                                        netlist_file: str, target_device: str = "generic") -> Dict[str, Any]:
        """Run NextPNR place and route"""
        try:
            # Validate input with firewall
            process_data = {
                "type": "nextpnr_pnr",
                "user_id": user_id,
                "project_id": project_id,
                "netlist_file": netlist_file,
                "target_device": target_device
            }
            
            is_safe = await self.firewall.validate_process(f"nextpnr_{project_id}", process_data)
            if not is_safe:
                return {"status": "error", "message": "Security validation failed"}
            
            # Create project directory
            project_path = os.path.join(self.projects_dir, project_id)
            os.makedirs(project_path, exist_ok=True)
            
            # Run NextPNR
            cmd = [
                "nextpnr-generic",
                "--json", netlist_file,
                "--write", f"{project_path}/pnr_result.json",
                "--verbose"
            ]
            
            logger.info(f"Running NextPNR: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=project_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # Read PNR result
                pnr_result_file = f"{project_path}/pnr_result.json"
                pnr_content = {}
                if os.path.exists(pnr_result_file):
                    with open(pnr_result_file, "r") as f:
                        pnr_content = json.load(f)
                
                result = {
                    "status": "success",
                    "project_id": project_id,
                    "pnr_output": stdout.decode(),
                    "pnr_errors": stderr.decode(),
                    "pnr_result": pnr_content
                }
                
                # Store result in Redis
                await redis_client.set_json(f"cad_result:nextpnr:{project_id}", result)
                
                await holo_misha_instance.notify_ar(
                    f"NextPNR place and route completed for project {project_id} by {user_id} - HoloMisha programs the universe!", 
                    "uk"
                )
                
                return result
            else:
                error_msg = stderr.decode()
                logger.error(f"NextPNR failed: {error_msg}")
                
                await holo_misha_instance.notify_ar(
                    f"NextPNR place and route failed for project {project_id} by {user_id}: {error_msg} - HoloMisha programs the universe!", 
                    "uk"
                )
                
                return {
                    "status": "error",
                    "message": "NextPNR place and route failed",
                    "error_details": error_msg
                }
                
        except Exception as e:
            logger.error(f"Error in NextPNR place and route: {e}")
            
            await holo_misha_instance.notify_ar(
                f"NextPNR place and route error for project {project_id} by {user_id}: {str(e)} - HoloMisha programs the universe!", 
                "uk"
            )
            
            return {
                "status": "error",
                "message": f"NextPNR place and route error: {str(e)}"
            }
    
    async def get_tool_versions(self) -> Dict[str, str]:
        """Get versions of all available CAD tools"""
        versions = {}
        
        for tool_name, tool_path in self.supported_tools.items():
            try:
                if await self.check_tool_availability(tool_name):
                    # Get version
                    if tool_name == "verilator":
                        cmd = [tool_path, "--version"]
                    elif tool_name == "yosys":
                        cmd = [tool_path, "-V"]
                    elif tool_name == "nextpnr":
                        cmd = [tool_path, "--version"]
                    else:
                        cmd = [tool_path, "--version"]
                    
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    
                    stdout, stderr = await process.communicate()
                    versions[tool_name] = stdout.decode().strip() or stderr.decode().strip()
                else:
                    versions[tool_name] = "Not available"
            except Exception as e:
                versions[tool_name] = f"Error: {str(e)}"
        
        return versions

# Global CAD worker instance
cad_worker = CADWorker()

# Convenience functions
async def run_verilator_simulation(user_id: str, project_id: str, verilog_files: list, 
                                 top_module: str, simulation_time: int = 1000) -> Dict[str, Any]:
    """Run Verilator simulation"""
    return await cad_worker.run_verilator_simulation(user_id, project_id, verilog_files, top_module, simulation_time)

async def run_yosys_synthesis(user_id: str, project_id: str, verilog_files: list,
                            target_family: str = "generic") -> Dict[str, Any]:
    """Run Yosys synthesis"""
    return await cad_worker.run_yosys_synthesis(user_id, project_id, verilog_files, target_family)

async def run_nextpnr_place_and_route(user_id: str, project_id: str, 
                                    netlist_file: str, target_device: str = "generic") -> Dict[str, Any]:
    """Run NextPNR place and route"""
    return await cad_worker.run_nextpnr_place_and_route(user_id, project_id, netlist_file, target_device)

async def get_cad_tool_versions() -> Dict[str, str]:
    """Get versions of all CAD tools"""
    return await cad_worker.get_tool_versions()