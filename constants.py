"""Constants and custom exceptions for the Holiday Parks application."""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
PROMPT_FILE = PROJECT_ROOT / "prompt_holidaypark.yaml"
PROMPT_TEMPLATE_FILE = PROJECT_ROOT / "prompt_template.yaml"

# Environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-Coder-32B-Instruct")
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "openai")


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

def validate_env_variables():
    """Validate that required environment variables are set."""
    if not HF_TOKEN:
        raise ConfigurationError(
            "HF_TOKEN not found in environment variables. "
            "Please add it to your .env file."
        )
    
    print("✓ Environment variables loaded successfully")
    print(f"  - Model: {MODEL_NAME}")
    print(f"  - Search Provider: {SEARCH_PROVIDER}")

class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""
    pass