import json
import logging
from datetime import datetime
import hashlib
import asyncio
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def serialize_for_network(data: Any) -> str:
    return json.dumps(data)

def deserialize_from_network(data_str: str) -> Any:
    return json.loads(data_str)

def get_current_timestamp() -> str:
    return datetime.utcnow().isoformat()

async def hash_data(data: str, algorithm: str = "sha256") -> str:
    algorithms = {
        "sha256": hashlib.sha256,
        "sha3_256": hashlib.sha3_256,
        "blake2b": hashlib.blake2b
    }
    if algorithm not in algorithms:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    hash_obj = algorithms[algorithm]()
    hash_obj.update(data.encode('utf-8'))
    return hash_obj.hexdigest()

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)