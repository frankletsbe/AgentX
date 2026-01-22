"""Constants and custom exceptions for the Holiday Parks application."""

from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent
# We will import config inside functions that need it to avoid circular dependency
# with config_manager.py which imports constants.py

AVAILABLE_TOOLS = {
    "holiday_park_criteria": "SmolAgentX.tools.holiday_park_criteria",
    "prompt_builder": "SmolAgentX.tools.prompt_builder",
    "WebSearchTool": "smolagents.WebSearchTool",
    "DuckDuckGoSearchTool": "smolagents.DuckDuckGoSearchTool",
    "VisitWebpageTool": "smolagents.VisitWebpageTool"
}

TYPE_MAP = {
    "site": "site",
    "camping": "site",
    "campsite": "site",
    "camping site": "site",
    "caravan": "site",
    "caravan site": "site",
    "van site": "site",
    "caravan park": "site",
    "holiday park": "site",
    "holiday park site": "site",
    "powered site": "site",
    "powered sites": "site",
    "unpowered site": "site",
    "unpowered sites": "site",
    "sites": "site",
    "cabin": "cabin",
    "cabins": "cabin",
    "villa": "cabin",
    "cottage": "cabin",
    "bungalow": "cabin",
    "chalet": "cabin",
    "lodge": "cabin",
    "ensuite": "ensuite",
    "ensuite site": "ensuite"
}

FEATURE_MAP = {
    "pool": "pool",
    "swimming pool": "pool",
    "water park": "water_park",
    "slide": "water_park",
    "slides": "water_park",
    "water slide": "water_park",
    "splash": "splash_park",
    "splash park": "splash_park",
    "pillow": "jumping_pillow",
    "jumping pillow": "jumping_pillow",
    "playground": "playground",
    "play ground": "playground",
    "kids club": "kids_club",
    "activity": "kids_club",
    "activities": "kids_club",
    "dog": "pet_friendly",
    "pet": "pet_friendly",
    "pets": "pet_friendly",
    "dog friendly": "pet_friendly",
    "pet friendly": "pet_friendly",
    "wifi": "wifi",
    "wi-fi": "wifi",
    "internet": "wifi",
    "beach": "beach_access",
    "beach access": "beach_access",
    "store": "kiosk",
    "kiosk": "kiosk",
    "shop": "kiosk",
    "convenience store": "kiosk",
    "bbq": "bbq",
    "barbecue": "bbq",
    "camp kitchen": "camp_kitchen",
    "kitchen": "camp_kitchen",
    "laundry": "laundry",
    "dump point": "dump_point",
    "fire": "fire_pit",
    "fire pit": "fire_pit",
    "fires": "fire_pit",
    "campfire": "fire_pit"
}

HUGGINGFACE_COMPATIBLE_MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "codellama/CodeLlama-34b-Instruct-hf",
]

ABACUS_COMPATIBLE_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-4-turbo",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]


def get_output_folder(requirement_filename: str = None) -> Path:
    """
    Get the output folder path based on requirement filename.

    Args:
        requirement_filename: Name of the requirement YAML file (e.g., 'holiday-park.yaml')

    Returns:
        Path object for the output folder
    """
    from config_manager import config
    output_root = config.output_root # Use the output_root from the Config instance
    if requirement_filename:
        folder_name = Path(requirement_filename).stem
        return output_root / folder_name
    return output_root / "default"


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""
    pass