import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Adjust sys.path to ensure imports work correctly for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Global Mocks for Config and its dependencies ---
# These need to be set up before any module that imports config_manager is loaded.

# Mock the global config instance itself
mock_config_instance = MagicMock()
# Patch the 'config' object within the 'config_manager' module
# This is crucial because agent_generic.py imports 'config' directly from 'config_manager'
# and config_manager's __init__ method is called on import.
patcher_config_manager_config = patch('config_manager.config', new=mock_config_instance)
patcher_config_manager_config.start() # Start the patch globally

# Mock the initialize_huggingface and initialize_abacus functions that config_manager calls
mock_initialize_huggingface = MagicMock()
mock_initialize_abacus = MagicMock()
patcher_init_hf = patch('agent_manager.initialize_huggingface', new=mock_initialize_huggingface)
patcher_init_abacus = patch('agent_manager.initialize_abacus', new=mock_initialize_abacus)
patcher_init_hf.start()
patcher_init_abacus.start()

# Mock YAMLConfigLoader and create_agent
mock_yaml_config_loader_instance = MagicMock()
mock_create_agent_func = MagicMock()

# Patch these within the agent_generic module namespace since they are imported there
patcher_yaml_loader = patch('agent_generic.YAMLConfigLoader', return_value=mock_yaml_config_loader_instance)
patcher_create_agent = patch('agent_generic.create_agent', new=mock_create_agent_func)
patcher_yaml_loader.start()
patcher_create_agent.start()

# Now import agent_generic.py's main function and ConfigurationError
from agent_generic import main as agent_generic_main, CONFIG_FILE
from constants import ConfigurationError

@pytest.fixture(autouse=True)
def setup_mocks():
    # Reset mocks before each test
    mock_config_instance.reset_mock()
    mock_initialize_huggingface.reset_mock()
    mock_initialize_abacus.reset_mock()
    mock_yaml_config_loader_instance.reset_mock()
    mock_create_agent_func.reset_mock()

    # Set up default mock behaviors for config
    mock_config_instance.get.side_effect = lambda key, default=None: {
        "INFERENCE_PROVIDER": "abacus",
        "MODEL_NAME": "mock-model",
        "SEARCH_PROVIDER": "mock-search",
        "API_TOKEN": "mock-api-token" # Ensure API_TOKEN is set for abacus provider
    }.get(key, default)
    mock_config_instance.get_list.return_value = ["WebSearchTool"]
    mock_config_instance._yaml_overrides = {} # For the debug print statement in agent_generic

    # Set up default mock behaviors for YAMLConfigLoader
    mock_yaml_config_loader_instance.load_prompt_with_template.return_value = "Mocked prompt query"
    mock_yaml_config_loader_instance.get_optional_config.return_value = None
    mock_yaml_config_loader_instance.get_config_list.return_value = ["WebSearchTool"]

    # Set up default mock behaviors for create_agent
    mock_agent_instance = MagicMock()
    mock_agent_instance.run.return_value = "Mocked agent response"
    mock_create_agent_func.return_value = mock_agent_instance

    yield # Run the test

# Stop global patches after all tests are done
def teardown_module(module):
    patcher_config_manager_config.stop()
    patcher_init_hf.stop()
    patcher_init_abacus.stop()
    patcher_yaml_loader.stop()
    patcher_create_agent.stop()


def test_agent_generic_success(capsys):
    """Test a successful run of agent_generic.py with Abacus provider."""
    agent_generic_main()

    captured = capsys.readouterr()
    assert "Welcome to the NSW Holiday Parks Review!" in captured.out
    assert "CONFIGURATION:" in captured.out
    assert "Provider: abacus [.env]" in captured.out
    assert "Model: mock-model [.env]" in captured.out
    assert "Search Provider: mock-search [.env]" in captured.out
    assert "Tools: WebSearchTool" in captured.out
    assert "PROMPT:" in captured.out
    assert "Mocked prompt query" in captured.out
    assert "Processing your query..." in captured.out
    assert "RESULTS:" in captured.out
    assert "Mocked agent response" in captured.out

    mock_config_instance.get.assert_any_call("INFERENCE_PROVIDER")
    mock_config_instance.get.assert_any_call("MODEL_NAME")
    mock_config_instance.get.assert_any_call("SEARCH_PROVIDER")
    mock_yaml_config_loader_instance.get_config_list.assert_called_once_with(CONFIG_FILE, "enabled_tools")
    mock_yaml_config_loader_instance.load_prompt_with_template.assert_called_once()
    mock_create_agent_func.assert_called_once_with(
        ["WebSearchTool"],
        model_id="mock-model",
        provider="abacus",
        search_provider="mock-search"
    )
    mock_create_agent_func.return_value.run.assert_called_once_with(task="Mocked prompt query")
    mock_initialize_abacus.assert_called_once()
    mock_initialize_huggingface.assert_not_called()


def test_agent_generic_success_huggingface(capsys):
    """Test a successful run of agent_generic.py with HuggingFace provider."""
    mock_config_instance.get.side_effect = lambda key, default=None: {
        "INFERENCE_PROVIDER": "huggingface",
        "MODEL_NAME": "mock-hf-model",
        "SEARCH_PROVIDER": "mock-hf-search",
        "HF_TOKEN": "mock-hf-token"
    }.get(key, default)
    mock_config_instance._yaml_overrides = {} # Reset for this test

    agent_generic_main()

    captured = capsys.readouterr()
    assert "Provider: huggingface [.env]" in captured.out
    assert "Model: mock-hf-model [.env]" in captured.out
    assert "Search Provider: mock-hf-search [.env]" in captured.out

    mock_create_agent_func.assert_called_once_with(
        ["WebSearchTool"],
        model_id="mock-hf-model",
        provider="huggingface",
        search_provider="mock-hf-search"
    )
    mock_initialize_huggingface.assert_called_once()
    mock_initialize_abacus.assert_not_called()


def test_agent_generic_configuration_error(capsys):
    """Test that ConfigurationError is handled gracefully."""
    mock_config_instance.get.side_effect = ConfigurationError("Test config error")

    agent_generic_main()

    captured = capsys.readouterr()
    assert "[ERROR] Configuration Error: Test config error" in captured.out
    # The first call to config.get("INFERENCE_PROVIDER") will raise the error
    mock_config_instance.get.assert_called_once_with("INFERENCE_PROVIDER")
    mock_create_agent_func.assert_not_called() # Agent should not be created


def test_agent_generic_unexpected_error(capsys):
    """Test that unexpected errors are handled gracefully."""
    mock_create_agent_func.side_effect = Exception("Unexpected agent creation error")

    agent_generic_main()

    captured = capsys.readouterr()
    assert "[ERROR] Unexpected Error: Unexpected agent creation error" in captured.out
    assert "Please check your configuration and try again." in captured.out
    mock_create_agent_func.assert_called_once() # Should be called before the error