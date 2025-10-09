import json
import os
from typing import Any, Dict

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config file: {e}")
        
        # Return default configuration
        return {
            "redis": {
                "host": "redis-master",
                "port": 6379
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000
            },
            "security": {
                "log_events": True,
                "notify_ar": True
            },
            "performance": {
                "simulation_delay": 0.1
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def reload(self):
        """Reload configuration from file"""
        self.config = self._load_config()

# Global config manager instance
config_manager = ConfigManager()