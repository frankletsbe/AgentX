"""Configuration loading utilities."""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

from constants import ConfigurationError, PROMPT_FILE, PROMPT_TEMPLATE_FILE


class YAMLConfigLoader:
    """Handles loading configuration from YAML files."""
    
    @staticmethod
    def load_prompt_with_template() -> str:
        """
        Load prompt from YAML and merge with template.
        
        Returns:
            Formatted prompt string
            
        Raises:
            ConfigurationError: If files are missing or invalid
        """
        try:
            # Load template values
            with open(PROMPT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
                template_config = yaml.safe_load(f)
                if not isinstance(template_config, dict):
                    raise ConfigurationError("Invalid template format")
            
            # Load prompt structure
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                prompt_values = yaml.safe_load(f)
                if not isinstance(prompt_values, dict):
                    raise ConfigurationError("Invalid prompt format")
            
            # Get prompt template string
            prompt_template = template_config.get("Prompt_Template", "")
            
            # Merge with overrides if present
            overrides = template_config.get("overrides", {})
            _values = {
                **template_config, 
                **{k: v for k, v in overrides.items() if v is not None}
            }
            
            # Format the prompt
            formatted_prompt = prompt_template.format(**prompt_values, **_values)

            
            return formatted_prompt
            
        except FileNotFoundError as e:
            raise ConfigurationError(f"Prompt file not found: {e.filename}")
        except KeyError as e:
            raise ConfigurationError(f"Missing template variable: {e}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML: {e}")
    
    @staticmethod
    def _load_yaml_file(file_path: Path) -> Dict[str, Any]:
        """
        Load and parse a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Parsed YAML content as dictionary
            
        Raises:
            ConfigurationError: If file not found or YAML parsing fails
        """
        
        if not file_path.exists():
            raise ConfigurationError(f"Configuration file not found: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                if content is None:
                    raise ConfigurationError(
                        f"Empty or invalid YAML file: {file_path}"
                    )
                if not isinstance(content, dict):
                    raise ConfigurationError(
                        f"Invalid YAML format in {file_path}. Expected a dictionary."
                    )
                return content
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {file_path}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML file {file_path}: {e}")
    
    @staticmethod
    def get_config_value(file_path: Path, key: str, default: str = "") -> str:
        """
        Get a value from a YAML configuration file.
        
        Args:
            file_path: Path to the YAML file
            key: Configuration key to retrieve
            default: Default value if key not found
            
        Returns:
            Configuration value as string
            
        Raises:
            ConfigurationError: If file is invalid
        """
        config = YAMLConfigLoader._load_yaml_file(file_path)
        value = config.get(key, default)
        return str(value) if value is not None else default
    
    @staticmethod
    def get_config_list(file_path: Path, key: str, default: Optional[List[str]] = None) -> List[str]:
        """
        Get a list configuration value from a YAML file.
        
        Args:
            file_path: Path to the YAML file
            key: Configuration key to retrieve
            default: Default value if key not found

        Returns:
            List of configuration values
        """
        if default is None:
            default = []

        config = YAMLConfigLoader._load_yaml_file(file_path)
        value = config.get(key, default)
        return value if isinstance(value, list) else default
    
    @staticmethod
    def get_optional_config(file_path: Path, key: str) -> Optional[str]:
        """
        Get an optional configuration value that can override environment variables.
        
        Args:
            file_path: Path to the YAML file
            key: Configuration key to retrieve
            
        Returns:
            Configuration value if present and not commented out, None otherwise
        """
        try:
            config = YAMLConfigLoader._load_yaml_file(file_path)
            value = config.get(key)
            # Return None if value is None, empty string, or explicitly set to null
            return str(value) if value not in (None, "", "null") else None
        except ConfigurationError:
            return None
