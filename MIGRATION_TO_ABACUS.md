# Migration from Hugging Face to Abacus.AI

## Summary of Changes

The codebase has been migrated from using Hugging Face models to Abacus.AI models. This provides access to multiple LLM providers through a single OpenAI-compatible API.

## Key Changes

### 1. **agent_manager.py**
- Removed `huggingface_hub` dependency
- Added `AbacusAIModel` class that extends `LiteLLMModel`
- Replaced `initialize_huggingface()` with `initialize_abacus()`
- Updated `create_agent()` to use Abacus.AI models via `routellm.abacus.ai` endpoint

### 2. **constants.py**
- Replaced `HF_TOKEN` with `ABACUS_API_KEY`
- Updated default `MODEL_NAME` from `Qwen/Qwen2.5-Coder-32B-Instruct` to `gpt-4o`
- Removed `SEARCH_PROVIDER` (no longer needed)
- Updated `validate_env_variables()` to check for `ABACUS_API_KEY`

### 3. **Agents/dev_team.py**
- Updated import from `initialize_huggingface` to `initialize_abacus`
- Updated function call to use new initialization method

## Setup Instructions

### 1. Get Your Abacus.AI API Key
1. Go to [Abacus.AI](https://abacus.ai)
2. Sign up or log in
3. Navigate to Settings → Profile & Billing
4. Click "Enable API Metering"
5. Go to API Keys and create a new key

### 2. Configure Environment Variables
Create a `.env` file in the project root:

```bash
# Abacus.AI Configuration
ABACUS_API_KEY=your_abacus_api_key_here

# Model Configuration
MODEL_NAME=gpt-4o
```

### 3. Available Models
Abacus.AI provides access to multiple models through their RouteLLM endpoint:
- `gpt-4o` (OpenAI)
- `gpt-4` (OpenAI)
- `claude-3-5-sonnet-20241022` (Anthropic)
- `claude-3-opus-20240229` (Anthropic)
- And many more...

Visit [https://routellm.abacus.ai](https://routellm.abacus.ai) for the full list.

## Benefits of Abacus.AI

1. **Multi-Provider Access**: Access models from OpenAI, Anthropic, Google, Meta, and more through a single API
2. **OpenAI-Compatible**: Uses standard OpenAI API format, making integration seamless
3. **Cost Optimization**: RouteLLM can automatically route requests to the most cost-effective model
4. **No Model Hosting**: No need to manage model deployments or infrastructure

## Migration Notes

- The API endpoint is `https://routellm.abacus.ai`
- Authentication uses standard API key in headers
- All existing tool integrations remain unchanged
- The `smolagents` library's `LiteLLMModel` handles the OpenAI-compatible interface

## Troubleshooting

If you encounter authentication errors:
1. Verify your `ABACUS_API_KEY` is set correctly in `.env`
2. Ensure API metering is enabled in your Abacus.AI account
3. Check that your API key has not expired

If you encounter model errors:
1. Verify the model name is correct (case-sensitive)
2. Check that the model is available in your Abacus.AI plan
3. Try using `gpt-4o` as a fallback
