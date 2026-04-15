"""Configuration management for gerrit-checkout."""

import configparser
from pathlib import Path
from typing import Dict, Any


def _clean_cfg_value(value: str) -> str:
    """Normalize config values by trimming whitespace and optional quotes."""
    return value.strip().strip("\"'").strip()


def load_config() -> Dict[str, Any]:
    """Load configuration from ~/.gerrit-checkout.cfg.
    
    Returns:
        Dictionary with configuration values
    """
    config_file = Path.home() / ".gerrit-checkout.cfg"
    config = {
        "gerrit_server": "",
        "repo_path": ".",
    }
    
    if not config_file.exists():
        return config
    
    try:
        parser = configparser.ConfigParser()
        parser.read(config_file)
        
        if parser.has_section("gerrit"):
            if parser.has_option("gerrit", "server"):
                config["gerrit_server"] = _clean_cfg_value(parser.get("gerrit", "server"))
            if parser.has_option("gerrit", "repo_path"):
                repo_path = _clean_cfg_value(parser.get("gerrit", "repo_path"))
                if repo_path:
                    config["repo_path"] = repo_path
    
    except Exception as e:
        print(f"Warning: Failed to load config file {config_file}: {e}")
    
    return config


def create_default_config(server: str = "") -> None:
    """Create ~/.gerrit-checkout.cfg with optional server override."""
    config_file = Path.home() / ".gerrit-checkout.cfg"

    existed_before = config_file.exists()
    server_input = _clean_cfg_value(server)
    existing = load_config() if existed_before else {"gerrit_server": "", "repo_path": "."}
    server_value = server_input or existing.get("gerrit_server", "") or "gerrit.exsample-com"
    repo_value = existing.get("repo_path", ".") or "."

    default_content = f"""[gerrit]
# Gerrit server hostname
server = {server_value}

# Default repository path (. for current directory)
repo_path = {repo_value}
"""

    try:
        config_file.write_text(default_content)
        action = "Updated" if existed_before else "Created"
        print(f"{action} config file: {config_file}")
        if server_input:
            print(f"  Server: {server_value}")
        elif server_value != "gerrit.exsample-com":
            print(f"  Server: {server_value}")
        else:
            print(f"  Server is set to the sample placeholder '{server_value}'.")
            print(f"  Edit {config_file} and replace it with your actual Gerrit hostname.")
            print(f"  Tip: next time run:  gerrit-checkout --init-config --gerrit-server YOUR_HOST")
    except Exception as e:
        print(f"Error: Failed to create config file {config_file}: {e}")
