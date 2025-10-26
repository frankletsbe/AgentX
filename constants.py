"""Constants and custom exceptions for the Holiday Parks application."""

from pathlib import Path

# File paths
CONFIG_FILE = Path("config.yaml")
PROMPT_FILE = Path("prompt.yaml")
PROMPT_TEMPLATE_FILE = Path("prompt_template.yaml")

# Type mappings
TYPE_MAP = {
    "site": "site",
    "camping": "site",
    "campsite": "site",
    "camping site": "site",
    "caravan": "site",
    "cabin": "cabin"
}


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""
    pass