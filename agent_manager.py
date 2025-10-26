"""Agent initialization and management."""

import importlib
from typing import List, Any
from huggingface_hub import login
from smolagents import CodeAgent, InferenceClientModel

from constants import ConfigurationError, AVAILABLE_TOOLS
#from tools import holiday_park_criteria, prompt_builder

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

def load_tool(tool_name: str) -> Any:
    """
    Dynamically load a tool by name.
    
    Args:
        tool_name: Name of the tool to load
        
    Returns:
        Tool instance or class
        
    Raises:
        ConfigurationError: If tool cannot be loaded
    """
    if tool_name not in AVAILABLE_TOOLS:
        raise ConfigurationError(f"Unknown tool: {tool_name}")
    
    tool_path = AVAILABLE_TOOLS[tool_name]
    module_name, attr_name = tool_path.rsplit(".", 1)
    
    try:
        module = importlib.import_module(module_name)
        tool = getattr(module, attr_name)
        
        # If it's a class (like SearchTool), instantiate it
        if isinstance(tool, type):
            return tool()
        return tool
        
    except (ImportError, AttributeError) as e:
        raise ConfigurationError(f"Failed to load tool '{tool_name}': {e}")

def create_agent(model_name: str, search_provider: str, tool_names: List[str]) -> CodeAgent:
    """
    Create and configure the AI agent with tools.
    
    Args:
        model_name: Name of the model to use
        search_provider: Search provider to use
        tool_names: List of tool names to enable
        
    Returns:
        Configured CodeAgent instance
        
    Raises:
        ConfigurationError: If agent creation fails
    """
    try:
        # Load tools dynamically
        tools = [load_tool(name) for name in tool_names]
        
        # Create agent
        client = InferenceClientModel(model_name, provider=search_provider)
        agent = CodeAgent(model=client, tools=tools)
        print(f"✓ Agent created with model: {model_name}")
        print(f"✓ Loaded tools: {', '.join(tool_names)}")
        
        return agent
    
    except Exception as e:
        raise ConfigurationError(f"Failed to create agent: {e}")