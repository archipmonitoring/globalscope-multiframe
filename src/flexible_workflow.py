"""
Flexible Workflow Engine for GlobalScope Innovation Nexus
Provides adaptable processes for different types of innovators and projects
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

from src.lib.utils import get_logger

logger = get_logger("FlexibleWorkflow")

class WorkflowType(Enum):
    """Types of innovation workflows"""
    BREAKTHROUGH = "breakthrough"  # Revolutionary innovations
    IMPROVEMENT = "improvement"    # Incremental improvements
    RESEARCH = "research"          # Scientific research
    SOCIAL = "social"              # Social impact projects
    DEFENSE = "defense"            # Defense applications
    HEALTHCARE = "healthcare"      # Medical innovations

class WorkflowStage(Enum):
    """Stages of innovation workflow"""
    CONCEPTION = "conception"
    PLANNING = "planning"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    IMPACT = "impact"

class FlexibleWorkflowEngine:
    """
    Adaptive workflow engine that provides flexible processes for different innovators
    """
    
    def __init__(self):
        self.workflows = {}
        self.workflow_templates = {}
        self.user_preferences = {}
        logger.info("FlexibleWorkflowEngine initialized")
    
    async def create_workflow_template(self, template_name: str, 
                                     workflow_type: WorkflowType,
                                     stages: List[WorkflowStage],
                                     customization_options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a customizable workflow template
        
        Args:
            template_name: Name of the workflow template
            workflow_type: Type of workflow
            stages: List of workflow stages
            customization_options: Options for customization
            
        Returns:
            Template creation status
        """
        try:
            template_id = f"template_{template_name.lower().replace(' ', '_')}"
            
            template = {
                "id": template_id,
                "name": template_name,
                "type": workflow_type.value,
                "stages": [stage.value for stage in stages],
                "customization_options": customization_options,
                "created_at": datetime.utcnow().isoformat(),
                "default_duration_days": customization_options.get("default_duration", 90),
                "human_centered": customization_options.get("human_centered", True),
                "collaborative": customization_options.get("collaborative", True)
            }
            
            self.workflow_templates[template_id] = template
            
            logger.info(f"Workflow template '{template_name}' created")
            return {
                "status": "success",
                "template_id": template_id,
                "message": f"Workflow template '{template_name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to create workflow template '{template_name}': {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create workflow template: {str(e)}"
            }
    
    async def create_custom_workflow(self, user_id: str, 
                                   template_id: str,
                                   project_name: str,
                                   customizations: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a custom workflow based on template
        
        Args:
            user_id: ID of the user creating the workflow
            template_id: Template to base the workflow on
            project_name: Name of the project
            customizations: User-specific customizations
            
        Returns:
            Workflow creation status
        """
        try:
            if template_id not in self.workflow_templates:
                return {
                    "status": "error",
                    "message": f"Template {template_id} not found"
                }
            
            template = self.workflow_templates[template_id]
            
            # Generate workflow ID
            workflow_id = f"workflow_{user_id}_{int(datetime.utcnow().timestamp())}"
            
            # Apply customizations
            workflow_config = template.copy()
            if customizations:
                for key, value in customizations.items():
                    workflow_config[key] = value
            
            # Create workflow
            workflow = {
                "id": workflow_id,
                "user_id": user_id,
                "project_name": project_name,
                "template_id": template_id,
                "config": workflow_config,
                "current_stage": WorkflowStage.CONCEPTION.value,
                "stage_progress": {},
                "created_at": datetime.utcnow().isoformat(),
                "started_at": None,
                "completed_at": None,
                "status": "created",
                "flexibility_score": 0.95  # High flexibility by default
            }
            
            self.workflows[workflow_id] = workflow
            self.user_preferences[user_id] = {
                "last_workflow": workflow_id,
                "preferred_template": template_id
            }
            
            logger.info(f"Custom workflow '{project_name}' created for user {user_id}")
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "message": f"Custom workflow '{project_name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to create custom workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create custom workflow: {str(e)}"
            }
    
    async def adapt_workflow(self, workflow_id: str, 
                           adaptation_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt workflow based on user needs or project changes
        
        Args:
            workflow_id: Workflow to adapt
            adaptation_request: Details about requested adaptations
            
        Returns:
            Adaptation status
        """
        try:
            if workflow_id not in self.workflows:
                return {
                    "status": "error",
                    "message": f"Workflow {workflow_id} not found"
                }
            
            workflow = self.workflows[workflow_id]
            
            # Apply adaptations
            adaptations_made = []
            
            # Stage modifications
            if "add_stage" in adaptation_request:
                new_stage = adaptation_request["add_stage"]
                if new_stage not in workflow["config"]["stages"]:
                    workflow["config"]["stages"].append(new_stage)
                    adaptations_made.append(f"Added stage: {new_stage}")
            
            if "remove_stage" in adaptation_request:
                remove_stage = adaptation_request["remove_stage"]
                if remove_stage in workflow["config"]["stages"]:
                    workflow["config"]["stages"].remove(remove_stage)
                    adaptations_made.append(f"Removed stage: {remove_stage}")
            
            # Duration modifications
            if "extend_duration" in adaptation_request:
                extension_days = adaptation_request["extend_duration"]
                workflow["config"]["default_duration_days"] += extension_days
                adaptations_made.append(f"Extended duration by {extension_days} days")
            
            # Flexibility enhancement
            if "increase_flexibility" in adaptation_request:
                workflow["flexibility_score"] = min(1.0, workflow["flexibility_score"] + 0.05)
                adaptations_made.append("Increased flexibility")
            
            # Update workflow
            workflow["last_adapted"] = datetime.utcnow().isoformat()
            workflow["adaptations"] = workflow.get("adaptations", []) + adaptations_made
            
            logger.info(f"Workflow {workflow_id} adapted: {', '.join(adaptations_made)}")
            return {
                "status": "success",
                "adaptations_made": adaptations_made,
                "message": "Workflow adapted successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to adapt workflow {workflow_id}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to adapt workflow: {str(e)}"
            }
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get current status of workflow
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Workflow status
        """
        try:
            if workflow_id not in self.workflows:
                return {
                    "status": "error",
                    "message": f"Workflow {workflow_id} not found"
                }
            
            workflow = self.workflows[workflow_id]
            
            return {
                "status": "success",
                "workflow": workflow
            }
            
        except Exception as e:
            logger.error(f"Failed to get workflow status: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get workflow status: {str(e)}"
            }
    
    async def advance_workflow_stage(self, workflow_id: str, 
                                   stage_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Advance workflow to next stage
        
        Args:
            workflow_id: Workflow identifier
            stage_data: Data related to current stage completion
            
        Returns:
            Stage advancement status
        """
        try:
            if workflow_id not in self.workflows:
                return {
                    "status": "error",
                    "message": f"Workflow {workflow_id} not found"
                }
            
            workflow = self.workflows[workflow_id]
            current_stage = workflow["current_stage"]
            stages = workflow["config"]["stages"]
            
            # Record current stage completion
            workflow["stage_progress"][current_stage] = {
                "completed": True,
                "completed_at": datetime.utcnow().isoformat(),
                "data": stage_data or {}
            }
            
            # Determine next stage
            current_index = stages.index(current_stage)
            if current_index < len(stages) - 1:
                next_stage = stages[current_index + 1]
                workflow["current_stage"] = next_stage
                workflow["stage_progress"][next_stage] = {
                    "started": True,
                    "started_at": datetime.utcnow().isoformat()
                }
                
                message = f"Workflow advanced to stage: {next_stage}"
            else:
                # Workflow completed
                workflow["current_stage"] = "completed"
                workflow["completed_at"] = datetime.utcnow().isoformat()
                workflow["status"] = "completed"
                message = "Workflow completed successfully"
            
            logger.info(f"Workflow {workflow_id} advanced: {message}")
            return {
                "status": "success",
                "message": message,
                "current_stage": workflow["current_stage"]
            }
            
        except Exception as e:
            logger.error(f"Failed to advance workflow {workflow_id}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to advance workflow: {str(e)}"
            }
    
    async def create_adaptive_templates(self):
        """Create default adaptive workflow templates"""
        # Breakthrough Innovation Template
        await self.create_workflow_template(
            "Breakthrough Innovation",
            WorkflowType.BREAKTHROUGH,
            [
                WorkflowStage.CONCEPTION,
                WorkflowStage.PLANNING,
                WorkflowStage.DEVELOPMENT,
                WorkflowStage.TESTING,
                WorkflowStage.DEPLOYMENT,
                WorkflowStage.IMPACT
            ],
            {
                "default_duration": 180,
                "human_centered": True,
                "collaborative": True,
                "research_intensive": True,
                "risk_tolerance": "high"
            }
        )
        
        # Social Impact Template
        await self.create_workflow_template(
            "Social Impact Project",
            WorkflowType.SOCIAL,
            [
                WorkflowStage.CONCEPTION,
                WorkflowStage.PLANNING,
                WorkflowStage.DEVELOPMENT,
                WorkflowStage.TESTING,
                WorkflowStage.DEPLOYMENT,
                WorkflowStage.IMPACT
            ],
            {
                "default_duration": 120,
                "human_centered": True,
                "community_engagement": True,
                "sustainability_focus": True,
                "accessibility_required": True
            }
        )
        
        # Defense Application Template
        await self.create_workflow_template(
            "Defense Application",
            WorkflowType.DEFENSE,
            [
                WorkflowStage.CONCEPTION,
                WorkflowStage.PLANNING,
                WorkflowStage.DEVELOPMENT,
                WorkflowStage.TESTING,
                WorkflowStage.DEPLOYMENT,
                WorkflowStage.IMPACT
            ],
            {
                "default_duration": 150,
                "security_required": True,
                "reliability_target": 0.9999,
                "quality_assurance": "maximum",
                "compliance_required": True
            }
        )
        
        logger.info("Adaptive workflow templates created")

# Global instance
flexible_workflow = FlexibleWorkflowEngine()