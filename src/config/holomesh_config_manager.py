"""
Менеджер конфігурації HoloMesh для CAD AI оптимізації

Цей модуль забезпечує завантаження, валідацію та доступ до конфігурації HoloMesh.
"""

import json
import os
from typing import Dict, Any, Optional
from src.lib.utils import get_logger

logger = get_logger("HoloMeshConfigManager")

class HoloMeshConfigManager:
    """Менеджер конфігурації HoloMesh."""
    
    def __init__(self, config_path: str = "config/holomesh_config.json"):
        """
        Ініціалізує менеджер конфігурації HoloMesh.
        
        Args:
            config_path: Шлях до файлу конфігурації
        """
        self.config_path = config_path
        self.config_data = {}
        self._load_config()
    
    def _load_config(self):
        """Завантажує конфігурацію з файлу."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                logger.info(f"Конфігурацію HoloMesh завантажено з {self.config_path}")
            else:
                logger.warning(f"Файл конфігурації не знайдено: {self.config_path}")
                self.config_data = self._get_default_config()
        except Exception as e:
            logger.error(f"Помилка завантаження конфігурації: {e}")
            self.config_data = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Повертає конфігурацію за замовчуванням."""
        return {
            "holomesh": {
                "api_version": "2.0",
                "interaction_modes": {
                    "professional": {
                        "description": "Standard mode for general CAD optimization tasks",
                        "default_confidentiality": True
                    },
                    "innovative": {
                        "description": "Creative exploration and experimental optimization",
                        "default_confidentiality": True
                    },
                    "semi_automatic": {
                        "description": "Human-AI collaboration with easy tool switching",
                        "default_confidentiality": True
                    },
                    "manual": {
                        "description": "Professional tool guidance with confidentiality controls",
                        "default_confidentiality": True
                    }
                }
            }
        }
    
    def get_interaction_mode_config(self, mode: str) -> Dict[str, Any]:
        """
        Отримує конфігурацію для конкретного режиму взаємодії.
        
        Args:
            mode: Назва режиму взаємодії
            
        Returns:
            Конфігурація режиму взаємодії
        """
        return self.config_data.get("holomesh", {}).get("interaction_modes", {}).get(mode, {})
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """
        Отримує конфігурацію для конкретного інструменту.
        
        Args:
            tool_name: Назва інструменту
            
        Returns:
            Конфігурація інструменту
        """
        return self.config_data.get("tools", {}).get(tool_name, {})
    
    def is_holomesh_integration_enabled(self, mode: str) -> bool:
        """
        Перевіряє, чи увімкнено інтеграцію HoloMesh для режиму.
        
        Args:
            mode: Назва режиму взаємодії
            
        Returns:
            True, якщо інтеграція увімкнена, інакше False
        """
        mode_config = self.get_interaction_mode_config(mode)
        return mode_config.get("holomesh_integration", False)
    
    def get_default_confidentiality(self, mode: str) -> bool:
        """
        Отримує налаштування конфіденційності за замовчуванням для режиму.
        
        Args:
            mode: Назва режиму взаємодії
            
        Returns:
            Значення конфіденційності за замовчуванням
        """
        mode_config = self.get_interaction_mode_config(mode)
        return mode_config.get("default_confidentiality", True)
    
    def get_recommendation_config(self) -> Dict[str, Any]:
        """
        Отримує конфігурацію рекомендацій.
        
        Returns:
            Конфігурація рекомендацій
        """
        return self.config_data.get("holomesh", {}).get("recommendations", {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """
        Отримує конфігурацію продуктивності.
        
        Returns:
            Конфігурація продуктивності
        """
        return self.config_data.get("holomesh", {}).get("performance", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Отримує конфігурацію логування.
        
        Returns:
            Конфігурація логування
        """
        return self.config_data.get("logging", {})
    
    def get_supported_modes_for_tool(self, tool_name: str) -> list:
        """
        Отримує список підтримуваних режимів для інструменту.
        
        Args:
            tool_name: Назва інструменту
            
        Returns:
            Список підтримуваних режимів
        """
        tool_config = self.get_tool_config(tool_name)
        return tool_config.get("supported_modes", ["professional"])
    
    def get_default_parameters_for_tool(self, tool_name: str) -> Dict[str, Any]:
        """
        Отримує параметри за замовчуванням для інструменту.
        
        Args:
            tool_name: Назва інструменту
            
        Returns:
            Параметри за замовчуванням
        """
        tool_config = self.get_tool_config(tool_name)
        return tool_config.get("default_parameters", {})
    
    def reload_config(self):
        """Перезавантажує конфігурацію з файлу."""
        logger.info("Перезавантаження конфігурації HoloMesh")
        self._load_config()
    
    def get_full_config(self) -> Dict[str, Any]:
        """
        Отримує повну конфігурацію.
        
        Returns:
            Повна конфігурація
        """
        return self.config_data

    def get_tool_parameter_ranges(self, tool_name: str) -> Dict[str, Any]:
        """
        Отримує діапазони параметрів для конкретного інструменту.
        
        Args:
            tool_name: Назва інструменту
            
        Returns:
            Діапазони параметріінструменту
        """
        tool_config = self.get_tool_config(tool_name)
        return tool_config.get("parameter_ranges", {})

    def get_tool_optimization_profiles(self, tool_name: str) -> Dict[str, Any]:
        """
        Отримує профілі оптимізації для конкретного інструменту.
        
        Args:
            tool_name: Назва інструменту
            
        Returns:
            Профілі оптимізації інструменту
        """
        tool_config = self.get_tool_config(tool_name)
        return tool_config.get("optimization_profiles", {})

    def get_optimization_profile(self, tool_name: str, profile_name: str) -> Dict[str, Any]:
        """
        Отримує конкретний профіль оптимізації для інструменту.
        
        Args:
            tool_name: Назва інструменту
            profile_name: Назва профілю
            
        Returns:
            Параметри профілю оптимізації
        """
        profiles = self.get_tool_optimization_profiles(tool_name)
        return profiles.get(profile_name, {})

# Глобальний екземпляр менеджера конфігурації
_holomesh_config_manager: Optional[HoloMeshConfigManager] = None

def get_holomesh_config_manager() -> HoloMeshConfigManager:
    """
    Отримує глобальний екземпляр менеджера конфігурації HoloMesh.
    
    Returns:
        Екземпляр HoloMeshConfigManager
    """
    global _holomesh_config_manager
    if _holomesh_config_manager is None:
        _holomesh_config_manager = HoloMeshConfigManager()
    return _holomesh_config_manager

def init_holomesh_config_manager(config_path: str = "config/holomesh_config.json") -> HoloMeshConfigManager:
    """
    Ініціалізує глобальний екземпляр менеджера конфігурації HoloMesh.
    
    Args:
        config_path: Шлях до файлу конфігурації
        
    Returns:
        Екземпляр HoloMeshConfigManager
    """
    global _holomesh_config_manager
    _holomesh_config_manager = HoloMeshConfigManager(config_path)
    return _holomesh_config_manager