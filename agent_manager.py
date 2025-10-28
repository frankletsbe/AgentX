"""Agent initialization and management."""

import importlib
from typing import List, Any, Optional, Dict
from huggingface_hub import login
from smolagents import  ToolCallingAgent, InferenceClientModel,  CodeAgent, DuckDuckGoSearchTool, FinalAnswerPromptTemplate, FinalAnswerTool, FinalAnswerStep


from constants import (
    ConfigurationError, 
    AVAILABLE_TOOLS, 
    HF_TOKEN, 
    MODEL_NAME, 
    SEARCH_PROVIDER,
    validate_env_variables
)


class CustomInferenceClientModel(InferenceClientModel):
    """Custom wrapper to fix tool_choice parameter."""
    
    def __call__(self, messages, stop_sequences=None, grammar=None, tools=None, tool_choice=None):
        """Override to force tool_choice to 'auto' or 'none'."""
        # Force tool_choice to be either 'auto' or 'none'
        if tool_choice is not None and tool_choice not in ["auto", "none"]:
            tool_choice = "auto"
        
        return super().__call__(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools=tools,
            tool_choice=tool_choice
        )


def initialize_huggingface() -> None:
    """Initialize Hugging Face authentication using environment variables."""
    try:
        validate_env_variables()
        login(token=HF_TOKEN, add_to_git_credential=False)
        print("✓ Successfully authenticated with Hugging Face")
    except Exception as e:
        raise ConfigurationError(f"Failed to authenticate: {e}")


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
        
        if isinstance(tool, type):
            return tool()
        return tool
        
    except (ImportError, AttributeError) as e:
        raise ConfigurationError(f"Failed to load tool '{tool_name}': {e}")


def create_agent(tool_names: List[str]) -> CodeAgent:
    """
    Create and configure the AI agent with specified tools.
    Uses MODEL_NAME and SEARCH_PROVIDER from environment variables.
    
    Args:
        tool_names: List of tool names to enable
        
    Returns:
        Configured CodeAgent instance
        
    Raises:
        ConfigurationError: If agent creation fails
    """
    try:
        # Load tools dynamically
        tools = [load_tool(name) for name in tool_names]
        
       
        
        # Create custom model client with fixed tool_choice
        client = CustomInferenceClientModel(MODEL_NAME, provider=SEARCH_PROVIDER)
        agent = CodeAgent(model=client, tools=tools)
        
        print(f"✓ Agent created with model: {MODEL_NAME}")
        print(f"✓ Loaded tools: {', '.join(tool_names)}")
        print(f"✓ Agent type: {type(agent).__name__}")
        
        return agent
        
    except Exception as e:
        raise ConfigurationError(f"Failed to create agent: {e}")
    
    """def create_agent(tool_names: List[str]) -> ToolCallingAgent:
        
        Create and configure the AI agent with specified tools.
        Uses MODEL_NAME and SEARCH_PROVIDER from environment variables.
        
        Args:
            tool_names: List of tool names to enable
            
        Returns:
            Configured ToolCallingAgent instance
            
        Raises:
            ConfigurationError: If agent creation fails
        
        try:
            # Load tools dynamically
            tools = [load_tool(name) for name in tool_names]
            
        
            
            # Create custom model client with fixed tool_choice
            client = CustomInferenceClientModel(MODEL_NAME, provider=SEARCH_PROVIDER)
            agent = ToolAgent(model=client, tools=tools)
            
            print(f"✓ Agent created with model: {MODEL_NAME}")
            print(f"✓ Loaded tools: {', '.join(tool_names)}")
            print(f"✓ Agent type: {type(agent).__name__}")
            
            return agent
            
        except Exception as e:
            raise ConfigurationError(f"Failed to create agent: {e}")
    """