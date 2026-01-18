"""Agent initialization and management."""

import importlib
from typing import List, Any, Optional, Dict
from openai import OpenAI
from huggingface_hub import login
from smolagents import ToolCallingAgent, CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, InferenceClientModel


from constants import (
    ConfigurationError,
    AVAILABLE_TOOLS,
    INFERENCE_PROVIDER,
    API_TOKEN,
    MODEL_NAME,
    SEARCH_PROVIDER,
    validate_env_variables
)


class CustomInferenceClientModel(InferenceClientModel):
    """Custom wrapper to fix tool_choice parameter for Hugging Face."""
    
    def __call__(self, messages, stop_sequences=None, grammar=None, tools=None, tool_choice=None):
        """Override to force tool_choice to 'auto' or 'none'."""
        if tool_choice is not None and tool_choice not in ["auto", "none"]:
            tool_choice = "auto"
        
        return super().__call__(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools=tools,
            tool_choice=tool_choice
        )


class AbacusAIModel(LiteLLMModel):
    """Custom model wrapper for Abacus.AI using OpenAI-compatible API."""

    def __init__(self, model_id: str, api_key: str):
        # Map model names to what Abacus.AI expects
        # For CodeLLM, we use the route-llm default (empty model name)
        # For others, we use standard model names
        model_mapping = {
            "codellm": "gpt-4o",  # Use gpt-4o as default for CodeLLM
            "qwen": "gpt-4o",
            "claude": "claude-3-5-sonnet-20241022"
        }
        
        # Check if model_id needs mapping
        model_lower = model_id.lower()
        mapped_model = model_id
        
        # Check if it's one of our custom names that needs mapping
        for key, value in model_mapping.items():
            if key in model_lower:
                mapped_model = value
                break
        
        # LiteLLM requires 'openai/' prefix for custom OpenAI-compatible endpoints
        litellm_model = f"openai/{mapped_model}"

        super().__init__(
            model_id=litellm_model,
            api_key=api_key,
            api_base="https://routellm.abacus.ai"
        )





def initialize_huggingface() -> None:
    try:
        validate_env_variables()
        print("OK Successfully authenticated with Hugging Face")
    except Exception as e:
        raise ConfigurationError(f"Failed to authenticate with Hugging Face: {e}")


def initialize_abacus() -> None:
    try:
        if not API_TOKEN:
            raise ConfigurationError("ABACUS_API_KEY not found in environment variables")
        print("OK Successfully configured Abacus.AI authentication")
    except Exception as e:
        raise ConfigurationError(f"Failed to authenticate with Abacus.AI: {e}")


def initialize_provider() -> None:
    if INFERENCE_PROVIDER == "huggingface":
        initialize_huggingface()
    elif INFERENCE_PROVIDER == "abacus":
        initialize_abacus()
    else:
        raise ConfigurationError(f"Unknown provider: {INFERENCE_PROVIDER}")


def load_tool(tool_name: str) -> Any:
    if tool_name not in AVAILABLE_TOOLS:
        raise ConfigurationError(f"Unknown tool: {tool_name}")
    
    tool_path = AVAILABLE_TOOLS[tool_name]
    module_name, attr_name = tool_path.rsplit(".", 1)
    
    try:
        module = importlib.import_module(module_name)
        tool = getattr(module, attr_name)
        
        if isinstance(tool, type):
            return tool()
        return tool
        
    except (ImportError, AttributeError) as e:
        raise ConfigurationError(f"Failed to load tool '{tool_name}': {e}")


def create_agent(tool_names: List[str], model_id: str = None, provider: str = None, search_provider: str = None) -> CodeAgent:
    """
    Create an agent with the specified tools and optional specific model.
    
    Args:
        tool_names: List of tool names to load
        model_id: Optional model ID to use (defaults to MODEL_NAME from constants)
        provider: Optional provider override (defaults to INFERENCE_PROVIDER from constants)
        search_provider: Optional search provider override (defaults to SEARCH_PROVIDER from constants)
    """
    try:
        tools = [load_tool(name) for name in tool_names]
        
        # Default to global values if not provided
        target_model = model_id if model_id else MODEL_NAME
        target_provider = provider.lower() if provider else INFERENCE_PROVIDER
        target_search = search_provider if search_provider else SEARCH_PROVIDER
        
        if target_provider == "huggingface":
            # For Hugging Face, use InferenceClientModel
            model = CustomInferenceClientModel(target_model, provider=target_search)
            print(f"OK Agent created with Hugging Face model: {target_model}")
            print(f"   Search provider: {target_search}")
            
        elif target_provider == "abacus":
            model = AbacusAIModel(
                model_id=target_model,
                api_key=API_TOKEN
            )
            print(f"OK Agent created with Abacus.AI model: {target_model}")
            print(f"   Search provider: {target_search}")
            
        else:
            raise ConfigurationError(f"Unknown provider: {target_provider}")
        
        agent = CodeAgent(model=model, tools=tools)
        return agent
        
    except Exception as e:
        raise ConfigurationError(f"Failed to create agent: {e}")