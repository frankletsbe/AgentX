import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
# Import ConfigurationError and compatible model lists from constants (only static parts)
from constants import ConfigurationError, HUGGINGFACE_COMPATIBLE_MODELS, ABACUS_COMPATIBLE_MODELS

# We will import agent_manager inside the validation function to avoid circular dependency

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # Define base paths
        self.project_root = Path(__file__).parent
        self.output_root = self.project_root / "output"
        self.config_file = self.project_root / "config.yaml"
        self.prompt_file = self.project_root / "Requirements" / "holiday-park.yaml"
        self.prompt_template_file = self.project_root / "Requirements" / "template.yaml"

        load_dotenv() # Load .env variables once at the start

        # Load environment variables
        self._env_config = {
            "INFERENCE_PROVIDER": os.getenv("INFERENCE_PROVIDER", "abacus").lower(),
            "HF_MODEL_NAME": os.getenv("HF_MODEL_NAME", "Qwen/Qwen3-72B-Instruct-AWQ"),
            "HF_SEARCH_PROVIDER": os.getenv("HF_SEARCH_PROVIDER", "openai"),
            "HF_TOKEN": os.getenv("HF_TOKEN"),
            "AI_MODEL_NAME": os.getenv("AI_MODEL_NAME", "Qwen/Qwen3-72B-Instruct-AWQ"),
            "PLANNING_MODEL_NAME": os.getenv("PLANNING_MODEL_NAME", "Qwen/Qwen3-72B-Instruct-AWQ"),
            "AI_SEARCH_PROVIDER": os.getenv("AI_SEARCH_PROVIDER", "openai"),
            "AI_TOKEN": os.getenv("AI_TOKEN"),
            "ABACUS_API_KEY": os.getenv("ABACUS_API_KEY"), # Explicitly get ABACUS_API_KEY
        }
        
        # Load YAML overrides
        self._yaml_overrides = self._load_yaml_file(self.config_file)
        
        # Merge and finalize configuration
        self._final_config = self._merge_configs()
        
        # Validate and initialize the selected provider
        self._validate_and_initialize_provider()

    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a YAML file, returning an empty dict if not found or invalid."""
        try:
            if not file_path.exists():
                return {}
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                return content if isinstance(content, dict) else {}
        except yaml.YAMLError:
            print(f"Warning: Error parsing YAML file {file_path}. Ignoring overrides from this file.")
            return {}

    def _merge_configs(self) -> Dict[str, Any]:
        """Merge environment variables with YAML overrides."""
        merged = self._env_config.copy()
        
        # Apply YAML overrides for generic keys that can override provider-specific ones
        for key in ["INFERENCE_PROVIDER", "MODEL_NAME", "SEARCH_PROVIDER"]:
            yaml_value = self._yaml_overrides.get(key)
            if yaml_value is not None and str(yaml_value).lower() != "null":
                merged[key] = str(yaml_value)

        # Determine the active provider and set generic MODEL_NAME, SEARCH_PROVIDER, API_TOKEN
        provider = merged.get("INFERENCE_PROVIDER")
        if provider == "huggingface":
            # If MODEL_NAME was overridden in YAML, it takes precedence over HF_MODEL_NAME
            merged["MODEL_NAME"] = merged.get("MODEL_NAME") or merged["HF_MODEL_NAME"]
            merged["SEARCH_PROVIDER"] = merged.get("SEARCH_PROVIDER") or merged["HF_SEARCH_PROVIDER"]
            merged["API_TOKEN"] = merged["HF_TOKEN"]
        else: # Default to Abacus.AI or if explicitly set
            # If MODEL_NAME was overridden in YAML, it takes precedence over AI_MODEL_NAME
            merged["MODEL_NAME"] = merged.get("MODEL_NAME") or merged["AI_MODEL_NAME"]
            merged["SEARCH_PROVIDER"] = merged.get("SEARCH_PROVIDER") or merged["AI_SEARCH_PROVIDER"]
            merged["API_TOKEN"] = merged["AI_TOKEN"] or merged["ABACUS_API_KEY"] # Prefer AI_TOKEN, fallback to ABACUS_API_KEY

        # Ensure PLANNING_MODEL_NAME is set, potentially from AI_MODEL_NAME if not explicitly set
        if not merged.get("PLANNING_MODEL_NAME"):
            merged["PLANNING_MODEL_NAME"] = merged.get("AI_MODEL_NAME")

        # Add enabled_tools from YAML, if present
        enabled_tools = self._yaml_overrides.get("enabled_tools")
        if isinstance(enabled_tools, list):
            merged["enabled_tools"] = enabled_tools
        else:
            merged["enabled_tools"] = [] # Default to empty list if not specified

        return merged

    def _validate_and_initialize_provider(self):
        """Validate configuration and initialize the selected provider."""
        import agent_manager
        provider = self.get("INFERENCE_PROVIDER")
        model_name = self.get("MODEL_NAME")
        planning_model_name = self.get("PLANNING_MODEL_NAME")
        api_token = self.get("API_TOKEN")

        if provider not in ["huggingface", "abacus"]:
            raise ConfigurationError(f"Invalid INFERENCE_PROVIDER: {provider}")

        if provider == "huggingface":
            if not api_token:
                raise ConfigurationError("HF_TOKEN not found in environment variables. Please add it to your .env file.")
            if model_name not in HUGGINGFACE_COMPATIBLE_MODELS:
                print(f"Warning: Model '{model_name}' not in verified Hugging Face compatibility list. Attempting to use it anyway.")
            agent_manager.initialize_huggingface(self) # Pass self to avoid circular dependency
        elif provider == "abacus":
            if not api_token:
                raise ConfigurationError("AI_TOKEN or ABACUS_API_KEY not found in environment variables. Please add it to your .env file.")
            if model_name not in ABACUS_COMPATIBLE_MODELS:
                print(f"Warning: Model '{model_name}' not in verified Abacus.AI compatibility list. Attempting to use it anyway.")
            if planning_model_name and planning_model_name not in ABACUS_COMPATIBLE_MODELS:
                print(f"Warning: Planning Model '{planning_model_name}' not in verified Abacus.AI compatibility list. Attempting to use it anyway.")
            agent_manager.initialize_abacus(self) # Pass self to avoid circular dependency

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._final_config.get(key, default)

    def get_list(self, key: str, default: Optional[List[str]] = None) -> List[str]:
        """Get a list configuration value, primarily from YAML overrides."""
        value = self._final_config.get(key, default)
        return value if isinstance(value, list) else (default if default is not None else [])

# Global instance for easy access
config = Config()