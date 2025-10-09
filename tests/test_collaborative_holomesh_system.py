"""
Тести для колабораційної системи HoloMesh CAD AI

Цей файл містить комплексні тести для перевірки всієї системи
взаємодії HoloMesh у різних сценаріях командної роботи.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from src.ai.cad_ai_optimizer import (
    CADAIOptimizer, 
    AIOptimizationStrategy, 
    InteractionMode,
    CADParameterConfig
)

@pytest.fixture
def optimizer():
    """Створює екземпляр CADAIOptimizer для тестування."""
    return CADAIOptimizer()

@pytest.fixture
def team_scenarios():
    """Сценарії командної роботи."""
    return [
        {
            "name": "Senior Engineer Manual Mode",
            "role": "senior_engineer",
            "strategy": AIOptimizationStrategy.MANUAL,
            "mode": InteractionMode.MANUAL,
            "confidentiality": True
        },
        {
            "name": "Junior Engineer Semi-Automatic Mode",
            "role": "junior_engineer",
            "strategy": AIOptimizationStrategy.SEMI_AUTOMATIC,
            "mode": InteractionMode.SEMI_AUTOMATIC,
            "confidentiality": True
        },
        {
            "name": "R&D Specialist Innovative Mode",
            "role": "rd_specialist",
            "strategy": AIOptimizationStrategy.BAYESIAN,
            "mode": InteractionMode.INNOVATIVE,
            "confidentiality": True
        },
        {
            "name": "Professional Developer Professional Mode",
            "role": "professional_developer",
            "strategy": AIOptimizationStrategy.ENSEMBLE,
            "mode": InteractionMode.PROFESSIONAL,
            "confidentiality": True
        }
    ]

class TestCollaborativeHoloMeshSystem:
    """Тести для колабораційної системи HoloMesh."""
    
    @pytest.mark.asyncio
    async def test_team_collaboration_workflow(self, optimizer, team_scenarios):
        """Тест командного робочого процесу з різними режимами."""
        
        # Мокаємо необхідні методи
        with patch.object(optimizer, '_send_websocket_update'), \
             patch.object(optimizer, '_get_cached_optimal_config', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_cache', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_queue', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_websocket_manager', return_value=None):
            
            results = []
            
            # Імітуємо роботу кожної ролі в команді
            for scenario in team_scenarios:
                print(f"Тестуємо сценарій: {scenario['name']}")
                
                # Встановлюємо моки для специфічних методів
                if scenario['strategy'] == AIOptimizationStrategy.MANUAL:
                    with patch.object(optimizer, '_manual_optimization') as mock_manual:
                        mock_manual.return_value = {
                            "optimization_level": 3,
                            "abc_optimization": True
                        }
                        
                        result = await optimizer.optimize_cad_parameters(
                            tool_name="yosys",
                            project_id=f"test_project_{scenario['role']}",
                            initial_params={"optimization_level": 2},
                            target_metrics={"execution_time": 5.0},
                            strategy=scenario['strategy'],
                            max_iterations=10,
                            interaction_mode=scenario['mode'],
                            confidentiality_enabled=scenario['confidentiality']
                        )
                        
                        # Перевіряємо, що результат правильний
                        assert result["status"] == "success"
                        assert result["interaction_mode"] == scenario['mode'].value
                        assert result["confidentiality_enabled"] == scenario['confidentiality']
                        results.append(result)
                        
                elif scenario['strategy'] == AIOptimizationStrategy.SEMI_AUTOMATIC:
                    with patch.object(optimizer, '_semi_automatic_optimization') as mock_semi_auto:
                        mock_semi_auto.return_value = {
                            "placer": "heap",
                            "timing_driven": True
                        }
                        
                        result = await optimizer.optimize_cad_parameters(
                            tool_name="nextpnr",
                            project_id=f"test_project_{scenario['role']}",
                            initial_params={"placer": "sa"},
                            target_metrics={"quality_score": 0.9},
                            strategy=scenario['strategy'],
                            max_iterations=10,
                            interaction_mode=scenario['mode'],
                            confidentiality_enabled=scenario['confidentiality']
                        )
                        
                        # Перевіряємо, що результат правильний
                        assert result["status"] == "success"
                        assert result["interaction_mode"] == scenario['mode'].value
                        assert result["confidentiality_enabled"] == scenario['confidentiality']
                        results.append(result)
                        
                else:
                    # Для інших стратегій використовуємо базовий підхід
                    with patch.object(optimizer, '_bayesian_optimization') as mock_bayesian:
                        mock_bayesian.return_value = {
                            "optimization_level": 2,
                            "execution_time": 4.5
                        }
                        
                        result = await optimizer.optimize_cad_parameters(
                            tool_name="verilator",
                            project_id=f"test_project_{scenario['role']}",
                            initial_params={"optimization_level": 1},
                            target_metrics={"quality_score": 0.85},
                            strategy=scenario['strategy'],
                            max_iterations=10,
                            interaction_mode=scenario['mode'],
                            confidentiality_enabled=scenario['confidentiality']
                        )
                        
                        # Перевіряємо, що результат правильний
                        assert result["status"] == "success"
                        assert result["interaction_mode"] == scenario['mode'].value
                        assert result["confidentiality_enabled"] == scenario['confidentiality']
                        results.append(result)
            
            # Перевіряємо, що всі сценарії були протестовані
            assert len(results) == len(team_scenarios)
            
            # Перевіряємо, що всі результати успішні
            for result in results:
                assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_confidentiality_controls(self, optimizer):
        """Тест контролю конфіденційності в різних режимах."""
        
        # Мокаємо необхідні методи
        with patch.object(optimizer, '_manual_optimization') as mock_manual, \
             patch.object(optimizer, '_send_websocket_update'), \
             patch.object(optimizer, '_get_cached_optimal_config', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_cache', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_queue', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_websocket_manager', return_value=None):
            
            mock_manual.return_value = {"placer": "heap"}
            
            # Тест з конфіденційністю увімкненою
            result_conf_enabled = await optimizer.optimize_cad_parameters(
                tool_name="nextpnr",
                project_id="conf_test_001",
                initial_params={"placer": "sa"},
                target_metrics={"quality_score": 0.9},
                strategy=AIOptimizationStrategy.MANUAL,
                max_iterations=5,
                interaction_mode=InteractionMode.MANUAL,
                confidentiality_enabled=True
            )
            
            assert result_conf_enabled["status"] == "success"
            assert result_conf_enabled["confidentiality_enabled"] == True
            
            # Тест з конфіденційністю вимкненою
            result_conf_disabled = await optimizer.optimize_cad_parameters(
                tool_name="nextpnr",
                project_id="conf_test_002",
                initial_params={"placer": "sa"},
                target_metrics={"quality_score": 0.9},
                strategy=AIOptimizationStrategy.MANUAL,
                max_iterations=5,
                interaction_mode=InteractionMode.MANUAL,
                confidentiality_enabled=False
            )
            
            assert result_conf_disabled["status"] == "success"
            assert result_conf_disabled["confidentiality_enabled"] == False
    
    @pytest.mark.asyncio
    async def test_holomesh_integration_scenarios(self, optimizer):
        """Тест інтеграції HoloMesh в різних сценаріях."""
        
        # Налаштовуємо мок для інтерфейсу HoloMesh
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_recommendations.return_value = {
            "optimization_level": 3,
            "abc_optimization": True
        }
        optimizer.holomesh_interface.get_tool_guidance.return_value = {
            "placer": "heap",
            "timing_driven": True
        }
        
        # Тестуємо Semi-Automatic режим з інтеграцією HoloMesh
        semi_auto_result = await optimizer._semi_automatic_optimization(
            tool_name="yosys",
            initial_params={"optimization_level": 2},
            target_metrics={"execution_time": 5.0},
            interaction_mode=InteractionMode.SEMI_AUTOMATIC,
            process_id="test_semi_auto_001"
        )
        
        assert isinstance(semi_auto_result, dict)
        assert len(semi_auto_result) > 0
        optimizer.holomesh_interface.get_recommendations.assert_called_once()
        
        # Скидаємо мок для наступного тесту
        optimizer.holomesh_interface.reset_mock()
        
        # Тестуємо Manual режим з інтеграцією HoloMesh
        manual_result = await optimizer._manual_optimization(
            tool_name="nextpnr",
            initial_params={"placer": "sa"},
            target_metrics={"quality_score": 0.9},
            interaction_mode=InteractionMode.MANUAL,
            process_id="test_manual_001"
        )
        
        assert isinstance(manual_result, dict)
        assert len(manual_result) > 0
        optimizer.holomesh_interface.get_tool_guidance.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_project_database_collaboration(self, optimizer):
        """Тест співпраці через базу даних проектів."""
        
        # Додаємо дані проектів від різних учасників
        team_projects = [
            {
                "project_id": "senior_engineer_project",
                "tool_name": "yosys",
                "optimal_config": {"optimization_level": 3},
                "context": {"role": "senior_engineer", "confidentiality": "enabled"},
                "performance_metrics": {"execution_time": 4.2, "quality_score": 0.96},
                "chip_type": "FPGA",
                "technology_node": "28nm"
            },
            {
                "project_id": "junior_engineer_project",
                "tool_name": "nextpnr",
                "optimal_config": {"placer": "heap"},
                "context": {"role": "junior_engineer", "mode": "semi_automatic"},
                "performance_metrics": {"quality_score": 0.92, "resource_efficiency": 0.88},
                "chip_type": "FPGA",
                "technology_node": "28nm"
            }
        ]
        
        # Зберігаємо проекти в базі даних
        for project in team_projects:
            optimizer.project_database[project["project_id"]] = project
        
        # Перевіряємо, що проекти збережені
        assert len(optimizer.project_database) >= len(team_projects)
        
        # Тестуємо отримання рекомендацій на основі схожих проектів
        with patch('src.ai.cad_ai_optimizer.get_cad_cache', return_value=None):
            recommendations = await optimizer.get_recommendations(
                tool_name="yosys",
                project_context={"role": "new_engineer", "chip_type": "FPGA"}
            )
            
            assert recommendations["status"] == "success"
            assert "data" in recommendations

class TestCADParameterConfigCollaboration:
    """Тести для CADParameterConfig в контексті командної роботи."""
    
    def test_config_creation_for_different_roles(self):
        """Тест створення конфігурацій для різних ролей команди."""
        
        # Створюємо конфігурації для різних ролей
        configs = [
            CADParameterConfig(
                tool_name="yosys",
                parameters={"optimization_level": 3},
                performance_metrics={"execution_time": 4.2},
                project_context={"role": "senior_engineer"},
                interaction_mode="manual",
                confidentiality_enabled=True
            ),
            CADParameterConfig(
                tool_name="nextpnr",
                parameters={"placer": "heap"},
                performance_metrics={"quality_score": 0.92},
                project_context={"role": "junior_engineer"},
                interaction_mode="semi_automatic",
                confidentiality_enabled=True
            ),
            CADParameterConfig(
                tool_name="verilator",
                parameters={"language_extensions": "sv"},
                performance_metrics={"coverage": 0.95},
                project_context={"role": "rd_specialist"},
                interaction_mode="innovative",
                confidentiality_enabled=True
            )
        ]
        
        # Перевіряємо, що всі конфігурації створені правильно
        assert len(configs) == 3
        
        for i, config in enumerate(configs):
            assert config.tool_name is not None
            assert config.parameters is not None
            assert config.performance_metrics is not None
            assert config.project_context is not None
            assert config.interaction_mode is not None
            assert isinstance(config.confidentiality_enabled, bool)
            assert config.created_at > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])