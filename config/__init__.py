# config/__init__.py
import os
import configparser

def load_config() -> configparser.ConfigParser:
    config_dir = 'config'
    config_file = os.path.join(config_dir, 'config.ini')
    template_file = os.path.join(config_dir, 'configtemplate.ini')
    os.makedirs(config_dir, exist_ok=True)
    if not os.path.exists(config_file):
        if os.path.exists(template_file):
            with open(template_file, 'r') as template:
                content = template.read()
            with open(config_file, 'w') as config:
                config.write(content)
            print(f"Created {config_file} from {template_file}.")
        else:
            raise FileNotFoundError(f"Template file {template_file} not found.")
    config = configparser.ConfigParser()
    config.read(config_file)
    print('loaded config')
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
