# config/__init__.py
import os
import configparser
from typing import Dict

def load_config() -> configparser.ConfigParser:
    """Load and validate configuration from config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    config.read(config_path)
    _validate_config(config)
    return config

def _validate_config(config: configparser.ConfigParser) -> None:
    """Validate required configuration parameters"""
    required_sections = {
        'ALPHA_VANTAGE': ['api_key'],
        'REDDIT': ['client_id', 'client_secret', 'user_agent', 'subreddits']
    }
    
    for section, keys in required_sections.items():
        if section not in config:
            raise ValueError(f"Missing required section: {section}")
        
        for key in keys:
            if key not in config[section]:
                raise ValueError(f"Missing required key '{key}' in section '{section}'")
            if not config[section][key]:
                raise ValueError(f"Empty value for '{key}' in section '{section}'")

__all__ = ['load_config']
