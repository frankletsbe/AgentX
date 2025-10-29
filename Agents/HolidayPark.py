"""
Generic AI Agent Application
Loads configuration, prompt, and tools dynamically.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import ConfigurationError, CONFIG_FILE
from config_loader import YAMLConfigLoader
from agent_manager import initialize_huggingface, create_agent


def main() -> None:
    """Main entry point for the Holiday Parks Review application."""
    print("=" * 60)
    print("Welcome to the NSW Holiday Parks Review!")
    print("=" * 60)
    
    try:
        # Load configuration
        config_loader = YAMLConfigLoader()
        
        #token = config_loader.get_config_value(CONFIG_FILE, "HF_TOKEN")
        model_name = config_loader.get_config_value(CONFIG_FILE, "MODEL_NAME")
        search_provider = config_loader.get_config_value(CONFIG_FILE, "SEARCH_PROVIDER")
        enabled_tools = config_loader.get_config_list(CONFIG_FILE, "enabled_tools")
          
        # Load prompt with template
        query = config_loader.load_prompt_with_template()

      

# Debug output
        print("\n" + "=" * 60)
        print("CONFIGURATION:")
        print("=" * 60)
        print(f"Model: {model_name}")
        print(f"Provider: {search_provider}")
        print(f"Tools: {', '.join(enabled_tools)}")
        print("\n" + "=" * 60)
        print("PROMPT:")
        print("=" * 60)
        print(query)
        print("=" * 60 + "\n")
        
        # Initialize services
        initialize_huggingface()
        agent = create_agent(enabled_tools)

        # Run agent
        print("\nProcessing your query...")
        print("-" * 60)
        response = agent.run(task=query)
        
        print("\n" + "=" * 60)
        print("RESULTS:")
        print("=" * 60)
        print(response)
        
    except ConfigurationError as e:
        print(f"\n❌ Configuration Error: {e}")
        return
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("Please check your configuration and try again.")
        return


if __name__ == "__main__":
    main()