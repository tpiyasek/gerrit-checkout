"""Configuration management for gerrit-checkout."""

import configparser
from pathlib import Path
from typing import Optional, Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from ~/.gerrit-checkout.cfg.
    
    Returns:
        Dictionary with configuration values
    """
    config_file = Path.home() / ".gerrit-checkout.cfg"
    config = {
        "gerrit_server": "csp-gerrit-ssh.volvocars.net",
        "repo_path": ".",
    }
    
    if not config_file.exists():
        return config
    
    try:
        parser = configparser.ConfigParser()
        parser.read(config_file)
        
        if parser.has_section("gerrit"):
            if parser.has_option("gerrit", "server"):
                config["gerrit_server"] = parser.get("gerrit", "server")
            if parser.has_option("gerrit", "repo_path"):
                config["repo_path"] = parser.get("gerrit", "repo_path")
    
    except Exception as e:
        print(f"Warning: Failed to load config file {config_file}: {e}")
    
    return config


def create_default_config() -> None:
    """Create a default config file at ~/.gerrit-checkout.cfg."""
    config_file = Path.home() / ".gerrit-checkout.cfg"
    
    if config_file.exists():
        print(f"Config file already exists: {config_file}")
        return
    
    default_content = """[gerrit]
# Gerrit server hostname
server = csp-gerrit-ssh.volvocars.net

# Default repository path (. for current directory)
repo_path = .
"""
    
    try:
        config_file.write_text(default_content)
        print(f"Created config file: {config_file}")
    except Exception as e:
        print(f"Error: Failed to create config file {config_file}: {e}")
