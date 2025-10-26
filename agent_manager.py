"""Agent initialization and management."""

from huggingface_hub import login
from smolagents import CodeAgent, InferenceClientModel

from constants import ConfigurationError
from tools import holiday_park_criteria, prompt_builder

# Try WebSearchTool first; fall back to DuckDuckGoSearchTool if needed
try:
    from smolagents import WebSearchTool
    SearchTool = WebSearchTool
except ImportError:
    from smolagents import DuckDuckGoSearchTool as SearchTool


def initialize_huggingface(token: str) -> None:
    """
    Initialize Hugging Face authentication.
    
    Args:
        token: Hugging Face API token
        
    Raises:
        ConfigurationError: If authentication fails
    """
    try:
        login(token=token, add_to_git_credential=False)
        print("✓ Successfully authenticated with Hugging Face")
    except Exception as e:
        raise ConfigurationError(f"Failed to authenticate with Hugging Face: {e}")


def create_agent(model_name: str, search_provider: str) -> CodeAgent:
    """
    Create and configure the AI agent with tools.
    
    Args:
        model_name: Name of the model to use
        search_provider: Search provider to use
        
    Returns:
        Configured CodeAgent instance
        
    Raises:
        ConfigurationError: If agent creation fails
    """
    try:
        client = InferenceClientModel(model_name, provider=search_provider)
        tools = [holiday_park_criteria, prompt_builder, SearchTool()]
        agent = CodeAgent(model=client, tools=tools)
        print(f"✓ Agent created with model: {model_name}")
        return agent
    except Exception as e:
        raise ConfigurationError(f"Failed to create agent: {e}")