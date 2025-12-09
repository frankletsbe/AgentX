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
        # Map Qwen model names to Abacus model identifiers
        if "qwen" in model_id.lower():
            model_id = "Abacus.AI-Qwen3"

        super().__init__(
            model_id=model_id,
            api_key=api_key,
            api_base="https://routellm.abacus.ai"
        )


def initialize_huggingface() -> None:
    try:
        validate_env_variables()
        login(token=API_TOKEN, add_to_git_credential=False)
        print("✓ Successfully authenticated with Hugging Face")
    except Exception as e:
        raise ConfigurationError(f"Failed to authenticate with Hugging Face: {e}")


def initialize_abacus() -> None:
    try:
        validate_env_variables()
        if not API_TOKEN:
            raise ConfigurationError("ABACUS_API_KEY not found in environment variables")
        print("✓ Successfully configured Abacus.AI authentication")
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


def create_agent(tool_names: List[str], model_id: str = None) -> CodeAgent:
    """
    Create an agent with the specified tools and optional specific model.
    """
    try:
        tools = [load_tool(name) for name in tool_names]
        
        # Default to global MODEL_NAME if not provided
        target_model = model_id if model_id else MODEL_NAME
        
        if INFERENCE_PROVIDER == "huggingface":
            # For Hugging Face, we often map models differently or use the main one
            # If a specific Open AI model is requested on HF provider, we fallback to HF default
            if "gpt" in target_model.lower():
                target_model = MODEL_NAME
                
            model = CustomInferenceClientModel(target_model, provider=SEARCH_PROVIDER)
            print(f"✓ Agent created with Hugging Face model: {target_model}")
            
        elif INFERENCE_PROVIDER == "abacus":
            model = AbacusAIModel(
                model_id=target_model,
                api_key=API_TOKEN
            )
            print(f"✓ Agent created with Abacus.AI model: {target_model}")
            
        else:
            raise ConfigurationError(f"Unknown provider: {INFERENCE_PROVIDER}")
        
        agent = CodeAgent(model=model, tools=tools)
        return agent
        
    except Exception as e:
        raise ConfigurationError(f"Failed to create agent: {e}")