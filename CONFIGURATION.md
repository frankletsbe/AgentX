# Configuration Guide

This guide explains how to configure the AgentX application to use different AI providers, models, and search providers.

## Overview

AgentX supports two inference providers:

1. **HuggingFace** - Open-source models (Qwen, Llama, Mistral, etc.)
2. **Abacus.AI** - Proprietary models (GPT-4, Claude, Gemini, CodeLLM, etc.)

## Configuration Methods

There are **two ways** to configure the application:

### Method 1: Environment Variables (`.env` file)

This is the **primary** configuration method. Settings in `.env` are used by default.

### Method 2: YAML Overrides (`config.yaml`)

You can override `.env` settings by uncommenting values in `config.yaml`. This is useful for:

- Quick testing with different models
- Project-specific configurations
- Runtime overrides without changing `.env`

**Priority**: `config.yaml` overrides > `.env` defaults

---

## Quick Start Examples

### Example 1: Using HuggingFace (Qwen Model)

**Step 1**: Update `.env`:

```bash
INFERENCE_PROVIDER=huggingface
HF_TOKEN=your_huggingface_token_here
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=duckduckgo
```

**Step 2**: Run the app:

```bash
python app.py
```

### Example 2: Using Abacus.AI (CodeLLM)

**Step 1**: Update `.env`:

```bash
INFERENCE_PROVIDER=abacus
ABACUS_API_KEY=your_abacus_api_key_here
AI_TOKEN=your_abacus_api_key_here
AI_MODEL_NAME=CodeLLM
AI_SEARCH_PROVIDER=openai
```

**Step 2**: Run the app:

```bash
python app.py
```

### Example 3: Using Abacus.AI (GPT-4)

**Step 1**: Update `.env`:

```bash
INFERENCE_PROVIDER=abacus
ABACUS_API_KEY=your_abacus_api_key_here
AI_TOKEN=your_abacus_api_key_here
AI_MODEL_NAME=gpt-4o
AI_SEARCH_PROVIDER=openai
```

**Step 2**: Run the app:

```bash
python app.py
```

### Example 4: Using YAML Override (Quick Testing)

Keep your `.env` as-is, but test with a different model:

**Edit `config.yaml`**:

```yaml
# Uncomment to override .env settings
INFERENCE_PROVIDER: huggingface
MODEL_NAME: meta-llama/Llama-3.3-70B-Instruct
SEARCH_PROVIDER: duckduckgo
```

This will use HuggingFace with Llama model, overriding your `.env` settings.

---

## Detailed Configuration Reference

### Environment Variables (`.env`)

#### Provider Selection

```bash
# Options: "huggingface" or "abacus"
INFERENCE_PROVIDER=abacus
```

#### HuggingFace Configuration

```bash
# Your HuggingFace API token
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx

# Model name (must be a HuggingFace model)
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct

# Search provider for web searches
HF_SEARCH_PROVIDER=duckduckgo
```

**Available HuggingFace Models**:

- `Qwen/Qwen2.5-Coder-32B-Instruct` (recommended for coding)
- `meta-llama/Llama-3.1-8B-Instruct`
- `meta-llama/Llama-3.3-70B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `mistralai/Mixtral-8x7B-Instruct-v0.1`
- `codellama/CodeLlama-34b-Instruct-hf`

#### Abacus.AI Configuration

```bash
# Your Abacus.AI API key
ABACUS_API_KEY=s2_xxxxxxxxxxxxxxxxxxxxx
AI_TOKEN=s2_xxxxxxxxxxxxxxxxxxxxx

# Model name
AI_MODEL_NAME=CodeLLM

# Optional: Separate planning model
PLANNING_MODEL_NAME=CodeLLM

# Search provider for web searches
AI_SEARCH_PROVIDER=openai
```

**Available Abacus.AI Models**:

- `CodeLLM` (Abacus.AI's specialized coding model)
- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`
- `claude-3-5-sonnet-20241022`
- `claude-3-opus-20240229`
- `gemini-1.5-pro`
- `gemini-1.5-flash`

#### Search Providers

```bash
# Options: openai, serper, google, duckduckgo
HF_SEARCH_PROVIDER=duckduckgo
AI_SEARCH_PROVIDER=openai
```

### YAML Overrides (`config.yaml`)

To override `.env` settings, uncomment and set values in `config.yaml`:

```yaml
# ============================================================================
# OPTIONAL: RUNTIME CONFIGURATION OVERRIDES
# ============================================================================
# These settings override the .env file values if specified
# Leave commented out to use .env defaults

# Provider override (options: huggingface, abacus)
INFERENCE_PROVIDER: abacus

# Model name override
MODEL_NAME: CodeLLM

# Search provider override (options: openai, serper, google, duckduckgo)
SEARCH_PROVIDER: openai
```

---

## How Configuration is Loaded

The application loads configuration in this order:

1. **Load `.env` file** → Sets default values
2. **Check `config.yaml`** → Overrides `.env` if values are uncommented
3. **Display configuration** → Shows which source was used (`.env` or YAML override)

When you run the app, you'll see output like:

```
============================================================
CONFIGURATION:
============================================================
Provider: abacus [.env]
Model: CodeLLM [.env]
Search Provider: openai [.env]
Tools: holiday_park_criteria, prompt_builder, WebSearchTool
```

Or with overrides:

```
============================================================
CONFIGURATION:
============================================================
Provider: huggingface [YAML override]
Model: Qwen/Qwen2.5-Coder-32B-Instruct [YAML override]
Search Provider: duckduckgo [YAML override]
Tools: holiday_park_criteria, prompt_builder, WebSearchTool
```

---

## Getting API Keys

### HuggingFace Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token with "Read" permissions
3. Copy the token (starts with `hf_`)
4. Add to `.env` as `HF_TOKEN`

### Abacus.AI API Key

1. Go to [https://abacus.ai/](https://abacus.ai/)
2. Sign up or log in
3. Navigate to API settings
4. Generate a new API key (starts with `s2_`)
5. Add to `.env` as `ABACUS_API_KEY` and `AI_TOKEN`

---

## Troubleshooting

### Error: "HF_TOKEN not found in environment variables"

- Make sure you've set `HF_TOKEN` in your `.env` file
- Ensure `INFERENCE_PROVIDER=huggingface`

### Error: "AI_TOKEN not found in environment variables"

- Make sure you've set `AI_TOKEN` and `ABACUS_API_KEY` in your `.env` file
- Ensure `INFERENCE_PROVIDER=abacus`

### Model not working

- Check that the model name matches exactly (case-sensitive)
- For HuggingFace: Ensure the model is in the compatibility list
- For Abacus.AI: Verify your API key has access to the model

### Configuration not updating

- If using YAML overrides, make sure values are **uncommented** (no `#` at start)
- Check for typos in model names or provider names
- Restart the application after changing configuration

---

## Best Practices

1. **Use `.env` for secrets** - Never commit API keys to version control
2. **Use YAML for testing** - Quick model switching without changing `.env`
3. **Start with defaults** - Use the recommended models first
4. **Monitor costs** - Some Abacus.AI models (GPT-4, Claude) may incur costs
5. **Test locally** - Verify configuration before deploying

---

## Example Workflows

### Workflow 1: Development with Free Models

```bash
# .env
INFERENCE_PROVIDER=huggingface
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=duckduckgo
```

### Workflow 2: Production with Premium Models

```bash
# .env
INFERENCE_PROVIDER=abacus
AI_MODEL_NAME=gpt-4o
AI_SEARCH_PROVIDER=openai
```

### Workflow 3: Testing Different Models

```yaml
# config.yaml - Test without changing .env
INFERENCE_PROVIDER: abacus
MODEL_NAME: claude-3-5-sonnet-20241022
SEARCH_PROVIDER: openai
```

---

## Summary

- **Two providers**: HuggingFace (open-source) and Abacus.AI (proprietary)
- **Two configuration methods**: `.env` (default) and `config.yaml` (overrides)
- **Easy switching**: Change `INFERENCE_PROVIDER` to switch between providers
- **Flexible**: Override any setting via YAML for quick testing

For more help, see the main README or open an issue.
