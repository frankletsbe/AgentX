# Quick Configuration Examples

## Switch to HuggingFace

### Option 1: Edit `.env` file

```bash
INFERENCE_PROVIDER=huggingface
HF_TOKEN=your_token_here
HF_MODEL_NAME=Qwen/Qwen2.5-Coder-32B-Instruct
HF_SEARCH_PROVIDER=duckduckgo
```

### Option 2: Override in `config.yaml`

```yaml
# Uncomment these lines in config.yaml
INFERENCE_PROVIDER: huggingface
MODEL_NAME: Qwen/Qwen2.5-Coder-32B-Instruct
SEARCH_PROVIDER: duckduckgo
```

---

## Switch to Abacus.AI (CodeLLM)

### Option 1: Edit `.env` file

```bash
INFERENCE_PROVIDER=abacus
ABACUS_API_KEY=your_key_here
AI_TOKEN=your_key_here
AI_MODEL_NAME=CodeLLM
AI_SEARCH_PROVIDER=openai
```

### Option 2: Override in `config.yaml`

```yaml
# Uncomment these lines in config.yaml
INFERENCE_PROVIDER: abacus
MODEL_NAME: CodeLLM
SEARCH_PROVIDER: openai
```

---

## Switch to Abacus.AI (GPT-4)

### Option 1: Edit `.env` file

```bash
INFERENCE_PROVIDER=abacus
ABACUS_API_KEY=your_key_here
AI_TOKEN=your_key_here
AI_MODEL_NAME=gpt-4o
AI_SEARCH_PROVIDER=openai
```

### Option 2: Override in `config.yaml`

```yaml
# Uncomment these lines in config.yaml
INFERENCE_PROVIDER: abacus
MODEL_NAME: gpt-4o
SEARCH_PROVIDER: openai
```

---

## Switch to Abacus.AI (Claude)

### Option 1: Edit `.env` file

```bash
INFERENCE_PROVIDER=abacus
ABACUS_API_KEY=your_key_here
AI_TOKEN=your_key_here
AI_MODEL_NAME=claude-3-5-sonnet-20241022
AI_SEARCH_PROVIDER=openai
```

### Option 2: Override in `config.yaml`

```yaml
# Uncomment these lines in config.yaml
INFERENCE_PROVIDER: abacus
MODEL_NAME: claude-3-5-sonnet-20241022
SEARCH_PROVIDER: openai
```

---

## Verify Your Configuration

Run the app and check the output:

```bash
python app.py
```

You should see:

```
============================================================
CONFIGURATION:
============================================================
Provider: abacus [.env]
Model: CodeLLM [.env]
Search Provider: openai [.env]
Tools: holiday_park_criteria, prompt_builder, WebSearchTool
```

The `[.env]` or `[YAML override]` indicator shows which configuration source is being used.

---

## Troubleshooting

### "Provider not recognized"

- Check spelling: must be exactly `huggingface` or `abacus` (lowercase)

### "Model not found"

- Verify model name matches exactly (case-sensitive)
- Check that you're using a compatible model for your provider

### "API key not found"

- For HuggingFace: Set `HF_TOKEN` in `.env`
- For Abacus.AI: Set both `ABACUS_API_KEY` and `AI_TOKEN` in `.env`

### Configuration not updating

- If using YAML overrides, ensure lines are uncommented (no `#`)
- Restart the application after changes
- Check for typos in key names
