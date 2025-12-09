# Multi-Provider Support: Hugging Face & Abacus.AI

## Overview

The codebase supports both **Hugging Face** and **Abacus.AI** as inference providers with provider-prefixed configuration for easy switching.

## Quick Setup

### 1. Configure Your Provider

Edit your `.env` file and set the `INFERENCE_PROVIDER`:

```bash
# Choose your provider: "huggingface" or "abacus"
INFERENCE_PROVIDER=abacus
```

### 2. Provider-Specific Configuration

#### Option A: Using Abacus.AI (Recommended)

```bash
INFERENCE_PROVIDER=abacus

# Abacus.AI Configuration
AI_MODEL_NAME=gpt-4o
AI_SEARCH_PROVIDER=openai
AI_TOKEN=your_abacus_api_key_here
```

**Get Your Abacus.AI API Key:**
1. Go to [Abacus.AI](https://abacus.ai)
2. Sign up or log in
3. Navigate to Settings → Profile & Billing
4. Click "Enable API Metering"
5. Go to API Keys and create a new key

**Available Models:**
- `gpt-4o`, `gpt-4o-mini`, `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` (OpenAI)
- `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229` (Anthropic)
- `gemini-pro` (Google)
- And many more at [https://routellm.abacus.ai](https://routellm.abacus.ai)

#### Option B: Using Hugging Face

```bash
INFERENCE_PROVIDER=huggingface

# Hugging Face Configuration
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=openai
HF_TOKEN=your_huggingface_token_here
```

**Get Your Hugging Face Token:**
1. Go to [Hugging Face](https://huggingface.co)
2. Sign up or log in
3. Navigate to Settings → Access Tokens
4. Create a new token with read permissions

**Available Models:**
- `Qwen/Qwen2.5-Coder-32B-Instruct` (Coding specialist)
- `meta-llama/Llama-3.1-8B-Instruct`, `meta-llama/Llama-3.3-70B-Instruct` (Meta)
- `mistralai/Mistral-7B-Instruct-v0.2`, `mistralai/Mixtral-8x7B-Instruct-v0.1` (Mistral)
- `codellama/CodeLlama-34b-Instruct-hf` (Code-focused)

## Configuration Structure

### Provider-Prefixed Variables

All configuration uses provider-specific prefixes:

**Hugging Face:** `HF_*`
- `HF_MODEL_NAME` - Model to use
- `HF_SEARCH_PROVIDER` - Search provider (openai, huggingface)
- `HF_TOKEN` - Authentication token

**Abacus.AI:** `AI_*`
- `AI_MODEL_NAME` - Model to use
- `AI_SEARCH_PROVIDER` - Search provider
- `AI_TOKEN` - API key

### Benefits

✅ **No Conflicts** - Both providers can be configured simultaneously
✅ **Easy Switching** - Just change `INFERENCE_PROVIDER`
✅ **Clear Separation** - Each provider has its own namespace
✅ **Validation** - Automatic model compatibility checking

## Architecture

### Key Components

**agent_manager.py:**
- `initialize_provider()` - Automatically initializes the selected provider
- `initialize_huggingface()` - Hugging Face authentication
- `initialize_abacus()` - Abacus.AI authentication
- `create_agent()` - Creates agent with the appropriate model based on provider
- `CustomInferenceClientModel` - Wrapper for Hugging Face models
- `AbacusAIModel` - Wrapper for Abacus.AI models

**constants.py:**
- `INFERENCE_PROVIDER` - Provider selection ("huggingface" or "abacus")
- `HF_MODEL_NAME`, `HF_TOKEN`, `HF_SEARCH_PROVIDER` - Hugging Face settings
- `AI_MODEL_NAME`, `AI_TOKEN`, `AI_SEARCH_PROVIDER` - Abacus.AI settings
- `MODEL_NAME`, `API_TOKEN`, `SEARCH_PROVIDER` - Dynamically selected based on provider
- `validate_env_variables()` - Validates configuration and model compatibility
- `HUGGINGFACE_COMPATIBLE_MODELS` - List of verified HF models
- `ABACUS_COMPATIBLE_MODELS` - List of verified Abacus models

## Comparison

| Feature | Hugging Face | Abacus.AI |
|---------|-------------|-----------|
| **Model Access** | Open-source models | Multiple providers (OpenAI, Anthropic, Google, Meta) |
| **API Format** | Hugging Face Inference API | OpenAI-compatible |
| **Hosting** | Self-hosted or HF Inference | Fully managed |
| **Cost** | Free tier + paid inference | Pay-per-use |
| **Setup Complexity** | Moderate | Simple |
| **Model Variety** | Thousands of open models | Curated top models |

## Usage Examples

### Example 1: Using Abacus.AI with GPT-4

```bash
# .env
INFERENCE_PROVIDER=abacus
AI_TOKEN=sk-abacus-xxxxx
AI_MODEL_NAME=gpt-4o
```

### Example 2: Using Hugging Face with Qwen

```bash
# .env
INFERENCE_PROVIDER=huggingface
HF_TOKEN=hf_xxxxx
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=openai
```

### Example 3: Using Abacus.AI with Claude

```bash
# .env
INFERENCE_PROVIDER=abacus
AI_TOKEN=sk-abacus-xxxxx
AI_MODEL_NAME=claude-3-5-sonnet-20241022
```

## Switching Providers

To switch providers, simply update your `.env` file:

1. Change `INFERENCE_PROVIDER` to your desired provider
2. Ensure the corresponding provider-prefixed variables are set
3. Update the model name to a model available on that provider
4. Restart your application

No code changes required!

## Model Compatibility Validation

The system automatically validates model compatibility at startup:

### Hugging Face Compatible Models
- `Qwen/Qwen2.5-Coder-32B-Instruct`
- `meta-llama/Llama-3.1-8B-Instruct`
- `meta-llama/Llama-3.3-70B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `mistralai/Mixtral-8x7B-Instruct-v0.1`
- `codellama/CodeLlama-34b-Instruct-hf`

### Abacus.AI Compatible Models
- `gpt-4o`, `gpt-4o-mini`, `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`

**Note:** If you try to use an OpenAI/Anthropic model with Hugging Face provider, you'll get a clear error message with instructions to switch providers.

## Troubleshooting

### Hugging Face Issues

**Authentication Error:**
- Verify `HF_TOKEN` is set correctly in `.env`
- Check token has not expired
- Ensure token has read permissions

**Model Not Found:**
- Verify `HF_MODEL_NAME` is correct (case-sensitive)
- Check if model requires approval/gating
- Try a different model like `Qwen/Qwen2.5-Coder-32B-Instruct`

**Model Compatibility Error:**
- If you see "Model 'gpt-4o' is not available on Hugging Face"
- Change `INFERENCE_PROVIDER=abacus` in your `.env`
- Or use a Hugging Face model from the compatible list above

### Abacus.AI Issues

**Authentication Error:**
- Verify `AI_TOKEN` is set correctly in `.env`
- Ensure API metering is enabled in your account
- Check API key has not expired

**Model Not Found:**
- Verify `AI_MODEL_NAME` is correct (case-sensitive)
- Check model is available in your plan
- Try `gpt-4o` as a fallback

### General Issues

**Provider Not Recognized:**
- Ensure `INFERENCE_PROVIDER` is either "huggingface" or "abacus"
- Check for typos (case-insensitive)

**Missing Environment Variables:**
- Ensure all provider-prefixed variables are set for your chosen provider
- For Hugging Face: `HF_TOKEN`, `HF_MODEL_NAME`, `HF_SEARCH_PROVIDER`
- For Abacus.AI: `AI_TOKEN`, `AI_MODEL_NAME`

## Benefits of Each Provider

### Hugging Face
✅ Access to thousands of open-source models
✅ Free tier available
✅ Community-driven model ecosystem
✅ Fine-tuning capabilities
✅ Model versioning and control

### Abacus.AI
✅ Access to best commercial models (GPT-4, Claude, etc.)
✅ OpenAI-compatible API
✅ Automatic model routing for cost optimization
✅ No infrastructure management
✅ Single API for multiple providers
✅ Enterprise-grade reliability

## Migration Notes

The codebase automatically handles provider differences:
- Authentication methods
- API endpoints
- Model initialization
- Tool integration

All existing tools and agents work seamlessly with both providers.
