"""Constants and custom exceptions for the Holiday Parks application."""

from pathlib import Path

# File paths
CONFIG_FILE = Path("config.yaml")
PROMPT_FILE = Path("prompt_holidaypark.yaml")
PROMPT_TEMPLATE_FILE = Path("prompt_template.yaml")

# Available tool mappings
AVAILABLE_TOOLS = {
    "holiday_park_criteria": "tools.holiday_park_criteria",
    "prompt_builder": "tools.prompt_builder",
    "WebSearchTool": "smolagents.WebSearchTool",
    "DuckDuckGoSearchTool": "smolagents.DuckDuckGoSearchTool"
}

# Type mappings
# constants.py
TYPE_MAP = {
    # site-like
    "site": "site",
    "camping": "site",
    "campsite": "site",
    "camping site": "site",
    "caravan": "site",
    "caravan site": "site",
    "van site": "site",
    # caravan-park synonyms map to "site" or distinct category as needed
    "caravan park": "site",
    "holiday park": "site",
    "holiday park site": "site",
    "powered site": "site",
    "unpowered site": "site",
    # cabins
    "cabin": "cabin",
    "cabins": "cabin",
    "ensuite cabin": "cabin",
}


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""
    pass