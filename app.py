"""
Generic AI Agent Application
Loads configuration, prompt, and tools dynamically.
"""

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
        
        # Get configuration with YAML overrides (if specified in config.yaml)
        # These will override the .env values if present
        yaml_provider = config_loader.get_optional_config(CONFIG_FILE, "INFERENCE_PROVIDER")
        yaml_model = config_loader.get_optional_config(CONFIG_FILE, "MODEL_NAME")
        yaml_search = config_loader.get_optional_config(CONFIG_FILE, "SEARCH_PROVIDER")
        
        # Import constants after loading config to get environment variables
        from constants import (
            INFERENCE_PROVIDER as ENV_PROVIDER,
            MODEL_NAME as ENV_MODEL,
            SEARCH_PROVIDER as ENV_SEARCH
        )
        
        # Use YAML overrides if present, otherwise use environment variables
        provider = yaml_provider if yaml_provider else ENV_PROVIDER
        model_name = yaml_model if yaml_model else ENV_MODEL
        search_provider = yaml_search if yaml_search else ENV_SEARCH
        
        # Get enabled tools
        enabled_tools = config_loader.get_config_list(CONFIG_FILE, "enabled_tools")
          
        # Load prompt with template
        query = config_loader.load_prompt_with_template()

      

# Debug output
        print("\n" + "=" * 60)
        print("CONFIGURATION:")
        print("=" * 60)
        print(f"Provider: {provider}" + (" [YAML override]" if yaml_provider else " [.env]"))
        print(f"Model: {model_name}" + (" [YAML override]" if yaml_model else " [.env]"))
        print(f"Search Provider: {search_provider}" + (" [YAML override]" if yaml_search else " [.env]"))
        print(f"Tools: {', '.join(enabled_tools)}")
        print("\n" + "=" * 60)
        print("PROMPT:")
        print("=" * 60)
        print(query)
        print("=" * 60 + "\n")
        
        # Initialize services based on provider
        if provider.lower() == "huggingface":
            from agent_manager import initialize_huggingface
            initialize_huggingface()
        elif provider.lower() == "abacus":
            from agent_manager import initialize_abacus
            initialize_abacus()
        else:
            raise ConfigurationError(f"Unknown provider: {provider}")
        
        # Create agent with specified model, provider, and search provider
        from agent_manager import create_agent
        agent = create_agent(enabled_tools, model_id=model_name, provider=provider, search_provider=search_provider)

        # Run agent
        print("\nProcessing your query...")
        print("-" * 60)
        response = agent.run(task=query)
        
        print("\n" + "=" * 60)
        print("RESULTS:")
        print("=" * 60)
        print(response)
        
    except ConfigurationError as e:
        print(f"\n[ERROR] Configuration Error: {e}")
        return
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {e}")
        print("Please check your configuration and try again.")
        return


if __name__ == "__main__":
    main()