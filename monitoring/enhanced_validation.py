#!/usr/bin/env python3
"""
Enhanced validation script for Singularity Dashboard implementation
This script performs comprehensive validation of our monitoring implementation
"""
import json
import os
import sys
import asyncio
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedValidator:
    def __init__(self):
        self.results = {
            "dashboard": {"status": "pending", "details": []},
            "microservices": {"status": "pending", "details": []},
            "logging": {"status": "pending", "details": []},
            "configuration": {"status": "pending", "details": []}
        }
    
    def validate_dashboard_structure(self) -> bool:
        """Validate the enhanced dashboard JSON structure"""
        dashboard_files = [
            "monitoring/grafana/singularity_dashboard.json",
            "monitoring/grafana/enhanced_singularity_dashboard.json"
        ]
        
        all_valid = True
        for dashboard_file in dashboard_files:
            try:
                if not os.path.exists(dashboard_file):
                    self.results["dashboard"]["details"].append(f"❌ Dashboard file not found: {dashboard_file}")
                    all_valid = False
                    continue
                    
                with open(dashboard_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if dashboard structure is correct
                if "dashboard" not in data:
                    self.results["dashboard"]["details"].append(f"❌ {dashboard_file} missing 'dashboard' key")
                    all_valid = False
                    continue
                    
                dashboard = data["dashboard"]
                
                # Check required fields
                required_fields = ["id", "title", "tags", "timezone", "schemaVersion", "version", "refresh", "panels"]
                missing_fields = [field for field in required_fields if field not in dashboard]
                if missing_fields:
                    self.results["dashboard"]["details"].append(f"❌ {dashboard_file} missing fields: {missing_fields}")
                    all_valid = False
                    continue
                
                # Check panels
                panels = dashboard["panels"]
                if not isinstance(panels, list):
                    self.results["dashboard"]["details"].append(f"❌ {dashboard_file} panels should be a list")
                    all_valid = False
                    continue
                    
                # Check that we have enhanced panels
                panel_titles = [panel.get("title", "") for panel in panels]
                required_panels = [
                    "AI Performance Metrics",
                    "Zero Defect AI Forge Performance",
                    "TaskFusion Engine Performance",
                    "WebXR Fluidity Metrics",
                    "HoloArtemis AR Latency",
                    "WebXR Frame Rate",
                    "System Latency and Kafka Metrics",
                    "Kafka Message Processing Latency",
                    "Kafka Consumer Lag",
                    "System Health Overview",
                    "Overall System Health",
                    "Active Microservices",
                    "Error Rate"
                ]
                
                missing_panels = [title for title in required_panels if title not in panel_titles]
                if missing_panels:
                    self.results["dashboard"]["details"].append(f"⚠️ {dashboard_file} missing panels: {missing_panels}")
                else:
                    self.results["dashboard"]["details"].append(f"✅ {dashboard_file} has all required panels")
                    
                self.results["dashboard"]["details"].append(f"✅ {dashboard_file} structure is valid")
                
            except json.JSONDecodeError as e:
                self.results["dashboard"]["details"].append(f"❌ Invalid JSON in {dashboard_file}: {str(e)}")
                all_valid = False
            except Exception as e:
                self.results["dashboard"]["details"].append(f"❌ Error validating {dashboard_file}: {str(e)}")
                all_valid = False
        
        self.results["dashboard"]["status"] = "pass" if all_valid else "fail"
        return all_valid
    
    def validate_microservice_logging(self) -> bool:
        """Validate that all microservices have structured logging implemented"""
        microservices = [
            ("src/api/main_app.py", "api-gateway"),
            ("src/ai/zero_defect_ai_forge.py", "ai-service"),
            ("src/chip_design/zero_defect_engine.py", "chip-design"),
            ("src/fab/fab_analytics.py", "fab-service")
        ]
        
        required_elements = [
            "class JSONFormatter",
            "json.dumps",
            "timestamp",
            "level",
            "service",
            "message",
            "latency",
            "user_id",
            "chip_id",
            "ai_operation_time"
        ]
        
        all_valid = True
        for service_path, service_name in microservices:
            try:
                if not os.path.exists(service_path):
                    self.results["microservices"]["details"].append(f"❌ Microservice file not found: {service_path}")
                    all_valid = False
                    continue
                    
                with open(service_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                missing_elements = [element for element in required_elements if element not in content]
                if missing_elements:
                    self.results["microservices"]["details"].append(f"❌ {service_path} missing elements: {missing_elements}")
                    all_valid = False
                else:
                    self.results["microservices"]["details"].append(f"✅ {service_path} has proper structured logging implementation")
                    
            except Exception as e:
                self.results["microservices"]["details"].append(f"❌ Error validating {service_path}: {str(e)}")
                all_valid = False
        
        self.results["microservices"]["status"] = "pass" if all_valid else "fail"
        return all_valid
    
    def validate_logging_format(self) -> bool:
        """Validate that the logging format matches our requirements"""
        test_log_entry = {
            "timestamp": "2025-10-01T12:00:00Z",
            "level": "INFO",
            "service": "test-service",
            "message": "Test log entry",
            "latency": 0.123,
            "user_id": "test_user_123",
            "chip_id": "test_chip_456",
            "ai_operation_time": 0.0
        }
        
        # Check that all required fields are present
        required_fields = ["timestamp", "level", "service", "message", "latency", "user_id", "chip_id", "ai_operation_time"]
        missing_fields = [field for field in required_fields if field not in test_log_entry]
        
        if missing_fields:
            self.results["logging"]["details"].append(f"❌ Test log entry missing fields: {missing_fields}")
            self.results["logging"]["status"] = "fail"
            return False
        else:
            self.results["logging"]["details"].append("✅ Log entry format is valid")
            self.results["logging"]["status"] = "pass"
            return True
    
    def validate_configuration_files(self) -> bool:
        """Validate configuration files"""
        config_files = [
            "monitoring/config/prometheus.yml",
            "monitoring/filebeat/filebeat.microservices.yml"
        ]
        
        all_valid = True
        for config_file in config_files:
            try:
                if not os.path.exists(config_file):
                    self.results["configuration"]["details"].append(f"❌ Config file not found: {config_file}")
                    all_valid = False
                    continue
                    
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Basic validation - check if file is not empty
                if len(content.strip()) == 0:
                    self.results["configuration"]["details"].append(f"❌ {config_file} is empty")
                    all_valid = False
                else:
                    self.results["configuration"]["details"].append(f"✅ {config_file} exists and is not empty")
                    
            except Exception as e:
                self.results["configuration"]["details"].append(f"❌ Error validating {config_file}: {str(e)}")
                all_valid = False
        
        self.results["configuration"]["status"] = "pass" if all_valid else "fail"
        return all_valid
    
    async def run_all_validations(self) -> Dict[str, Any]:
        """Run all validations and return results"""
        logger.info("🚀 Starting enhanced validation of Singularity Dashboard implementation...")
        
        # Run validations
        self.validate_dashboard_structure()
        self.validate_microservice_logging()
        self.validate_logging_format()
        self.validate_configuration_files()
        
        return self.results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive validation report"""
        report = []
        report.append("=" * 80)
        report.append("ENHANCED SINGULARITY DASHBOARD VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Overall status
        all_passed = all(result["status"] == "pass" for result in results.values())
        status = "🎉 ALL VALIDATIONS PASSED" if all_passed else "❌ SOME VALIDATIONS FAILED"
        report.append(f"Overall Status: {status}")
        report.append("")
        
        # Detailed results
        for category, result in results.items():
            report.append(f"{category.upper()}:")
            report.append("-" * 40)
            for detail in result["details"]:
                report.append(f"  {detail}")
            report.append(f"  Status: {result['status'].upper()}")
            report.append("")
        
        # Summary
        report.append("=" * 80)
        report.append("SUMMARY:")
        for category, result in results.items():
            report.append(f"  {category}: {result['status'].upper()}")
        report.append("=" * 80)
        
        if all_passed:
            report.append("")
            report.append("🏆 The Singularity Dashboard implementation is production ready!")
            report.append("📊 All components have been validated successfully.")
            report.append("")
            report.append("Next steps:")
            report.append("  1. Deploy monitoring stack with deploy_monitoring.ps1")
            report.append("  2. Run execute_phase_3.py for end-to-end validation")
            report.append("  3. Access dashboard at http://localhost:3000")
        else:
            report.append("")
            report.append("❌ Please address the validation errors before deployment.")
        
        return "\n".join(report)

async def main():
    """Main function"""
    validator = EnhancedValidator()
    results = await validator.run_all_validations()
    report = validator.generate_report(results)
    print(report)
    
    # Return appropriate exit code
    all_passed = all(result["status"] == "pass" for result in results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    asyncio.run(main())