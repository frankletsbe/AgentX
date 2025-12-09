"""Constants and custom exceptions for the Holiday Parks application."""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).parent
OUTPUT_ROOT = PROJECT_ROOT / "output"
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
PROMPT_FILE = PROJECT_ROOT / "holiday-park.yaml"
PROMPT_TEMPLATE_FILE = PROJECT_ROOT / "template.yaml"

INFERENCE_PROVIDER = os.getenv("INFERENCE_PROVIDER", "abacus").lower()

HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "Qwen/Qwen2.5-Coder-32B-Instruct")
HF_SEARCH_PROVIDER = os.getenv("HF_SEARCH_PROVIDER", "openai")
HF_TOKEN = os.getenv("HF_TOKEN")

AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "gpt-4o")
AI_SEARCH_PROVIDER = os.getenv("AI_SEARCH_PROVIDER", "openai")
AI_TOKEN = os.getenv("AI_TOKEN")

CODING_MODEL_NAME = HF_MODEL_NAME if INFERENCE_PROVIDER == "huggingface" else AI_MODEL_NAME
CODING_SEARCH_PROVIDER = HF_SEARCH_PROVIDER if INFERENCE_PROVIDER == "huggingface" else AI_SEARCH_PROVIDER
CODING_API_TOKEN = HF_TOKEN if INFERENCE_PROVIDER == "huggingface" else AI_TOKEN

PLANNING_MODEL_NAME = os.getenv("PLANNING_MODEL_NAME", "gpt-4o")

AVAILABLE_TOOLS = {
    "WebSearchTool": "smolagents.WebSearchTool",
    "DuckDuckGoSearchTool": "smolagents.DuckDuckGoSearchTool"
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
    "gpt-3.5-turbo",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

def validate_env_variables():
    """Validate that required environment variables are set based on provider."""
    if INFERENCE_PROVIDER not in ["huggingface", "abacus"]:
        raise ConfigurationError(
            f"Invalid INFERENCE_PROVIDER: {INFERENCE_PROVIDER}. "
            "Must be 'huggingface' or 'abacus'"
        )

    if INFERENCE_PROVIDER == "huggingface":
        if not HF_TOKEN:
            raise ConfigurationError(
                "HF_TOKEN not found in environment variables. "
                "Please add it to your .env file."
            )

        if HF_MODEL_NAME not in HUGGINGFACE_COMPATIBLE_MODELS:
            if any(model_prefix in HF_MODEL_NAME.lower() for model_prefix in ["gpt", "claude"]):
                raise ConfigurationError(
                    f"Model '{HF_MODEL_NAME}' is not available on Hugging Face.\n"
                    f"This appears to be an OpenAI or Anthropic model.\n\n"
                    f"To use this model:\n"
                    f"  1. Change INFERENCE_PROVIDER to 'abacus' in your .env file\n"
                    f"  2. Ensure AI_TOKEN is set with your Abacus.AI API key\n\n"
                    f"Or use a Hugging Face model like:\n"
                    f"  - Qwen/Qwen2.5-Coder-32B-Instruct\n"
                    f"  - meta-llama/Llama-3.3-70B-Instruct\n"
                    f"  - mistralai/Mistral-7B-Instruct-v0.2"
                )
            print(f"⚠️  Warning: Model '{HF_MODEL_NAME}' not in verified compatibility list")
            print(f"   Attempting to use it anyway. If it fails, try a verified model.")

        print("✓ Environment variables loaded successfully")
        print(f"  - Provider: Hugging Face")
        print(f"  - Model: {HF_MODEL_NAME}")
        print(f"  - Search Provider: {HF_SEARCH_PROVIDER}")

    elif INFERENCE_PROVIDER == "abacus":
        if not AI_TOKEN:
            raise ConfigurationError(
                "AI_TOKEN not found in environment variables. "
                "Please add it to your .env file."
            )

        if AI_MODEL_NAME not in ABACUS_COMPATIBLE_MODELS:
            print(f"⚠️  Warning: Model '{AI_MODEL_NAME}' not in verified compatibility list")
            print(f"   Attempting to use it anyway. If it fails, try a verified model.")

        print("✓ Environment variables loaded successfully")
        print(f"  - Provider: Abacus.AI")
        print(f"  - Model: {AI_MODEL_NAME}")


def get_output_folder(requirement_filename: str = None) -> Path:
    """
    Get the output folder path based on requirement filename.

    Args:
        requirement_filename: Name of the requirement YAML file (e.g., 'holiday-park.yaml')

    Returns:
        Path object for the output folder
    """
    if requirement_filename:
        folder_name = Path(requirement_filename).stem
        return OUTPUT_ROOT / folder_name
    return OUTPUT_ROOT / "default"


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""
    pass
