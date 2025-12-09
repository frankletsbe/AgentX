# Quick Start: Provider Selection

## TL;DR

Choose your inference provider by setting `INFERENCE_PROVIDER` in your `.env` file:

### Abacus.AI (Recommended - Easy Setup)
```bash
INFERENCE_PROVIDER=abacus
AI_MODEL_NAME=gpt-4o
AI_TOKEN=your_key_here
```

### Hugging Face (Open Source Models)
```bash
INFERENCE_PROVIDER=huggingface
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_TOKEN=your_token_here
HF_SEARCH_PROVIDER=openai
```

## Get API Keys

**Abacus.AI:** https://abacus.ai → Settings → API Keys
**Hugging Face:** https://huggingface.co → Settings → Access Tokens

## Popular Models

### Abacus.AI (AI_MODEL_NAME)
- `gpt-4o` - Latest OpenAI model
- `gpt-4o-mini` - Faster, cheaper GPT-4
- `claude-3-5-sonnet-20241022` - Anthropic Claude
- `gpt-4` - OpenAI GPT-4

### Hugging Face (HF_MODEL_NAME)
- `Qwen/Qwen2.5-Coder-32B-Instruct` - Coding specialist
- `meta-llama/Llama-3.3-70B-Instruct` - Meta's Llama
- `meta-llama/Llama-3.1-8B-Instruct` - Smaller Llama
- `mistralai/Mistral-7B-Instruct-v0.2` - Mistral AI

## Configuration Structure

### Provider-Prefixed Variables

**Hugging Face:** All variables start with `HF_`
- `HF_MODEL_NAME` - Model to use
- `HF_TOKEN` - Authentication token
- `HF_SEARCH_PROVIDER` - Search provider (optional)

**Abacus.AI:** All variables start with `AI_`
- `AI_MODEL_NAME` - Model to use
- `AI_TOKEN` - API key
- `AI_SEARCH_PROVIDER` - Search provider (optional)

### Benefits
✅ Both providers can be configured at once
✅ Switch by changing `INFERENCE_PROVIDER` only
✅ No variable name conflicts
✅ Automatic model compatibility checking

## Complete .env Examples

### Abacus.AI Configuration
```bash
# Provider Selection
INFERENCE_PROVIDER=abacus

# Abacus.AI Settings
AI_MODEL_NAME=gpt-4o
AI_SEARCH_PROVIDER=openai
AI_TOKEN=your_abacus_api_key_here
```

### Hugging Face Configuration
```bash
# Provider Selection
INFERENCE_PROVIDER=huggingface

# Hugging Face Settings
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=openai
HF_TOKEN=your_huggingface_token_here
```

### Both Configured (Easy Switching)
```bash
# Provider Selection
INFERENCE_PROVIDER=abacus

# Hugging Face Settings
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=openai
HF_TOKEN=your_hf_token_here

# Abacus.AI Settings
AI_MODEL_NAME=gpt-4o
AI_SEARCH_PROVIDER=openai
AI_TOKEN=your_abacus_key_here
```

## Model Compatibility

### ⚠️ Important
- **Hugging Face** can only use models hosted on Hugging Face Hub
- **Abacus.AI** can use OpenAI, Anthropic, Google, and other models
- Using `gpt-4o` with `INFERENCE_PROVIDER=huggingface` will fail with a clear error

### Error Prevention
The system validates model compatibility at startup and provides helpful error messages if you try to use an incompatible model/provider combination.

## That's It!

No code changes needed. Just update `.env` and restart your app.

See `PROVIDER_SETUP.md` for detailed documentation.
