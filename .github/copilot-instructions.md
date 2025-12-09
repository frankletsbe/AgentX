# AgentX Copilot Instructions

## Project Overview
AgentX is a multi-agent AI development system that transforms YAML requirements into complete Python applications with deployment artifacts. It simulates a real development team with Business Analyst, Developer, UX Designer, QA Tester, and Manager agents coordinating work through structured feedback loops.

## Architecture & Core Components

### Multi-Agent System (Agents/)
- **AnalystAgent**: Transforms YAML requirements into detailed specifications (uses PLANNING_MODEL_NAME)
- **DeveloperAgent**: Writes production-ready Python code with error handling (uses AI_MODEL_NAME)
- **UXAgent**: Reviews interfaces and user flows (uses PLANNING_MODEL_NAME)
- **TesterAgent**: Reviews code quality, tests, and security (uses AI_MODEL_NAME)
- **ManagerAgent**: Orchestrates workflow, loads YAML from `Requirements/` directory, manages iteration loops (max 3 iterations)
- **DeepAgent**: Higher-level orchestrator that handles full YAML-to-application pipeline with DevOps output

### Critical Configuration
- **Provider abstraction**: Supports Abacus.AI and Hugging Face via `INFERENCE_PROVIDER` env var
- **Dual model strategy**: `PLANNING_MODEL_NAME` (Qwen3-72B) for analysis/design + `AI_MODEL_NAME` (Qwen3-72B) for coding
- **Model wrapping**: `CustomInferenceClientModel` handles HF tool_choice quirks; `AbacusAIModel` maps Qwen models to Abacus API
- **YAML-driven**: Requirements in `Requirements/*.yaml` are the single source of truth

## Key Development Workflows

### Running the Development Team
```bash
python run_deep_agent.py [optional/path/to/requirements.yaml]
```
Interactive mode selects from `Requirements/` directory; direct path skips selection.

### YAML Requirement Structure
```yaml
role: "Business Analyst"
task: "Analyze and create specifications"
requirements: "Define features, acceptance criteria, etc."
# Optional: tools, input_format, output_format
```

### Development Iteration Loop
1. **ManagerAgent.coordinate_development()** receives user requirement or YAML data
2. **AnalystAgent** → specification document
3. **DeveloperAgent** → code (receives spec + previous feedback)
4. **UXAgent** → UX feedback
5. **TesterAgent** → test feedback
6. **DeveloperAgent** (repeat) → iterates up to 3 times
7. Output saved to `output/` directory

### DeepAgent Pipeline (YAML → Full Application)
- Processes YAML as single source of truth
- Generates structured output: `src/`, `tests/`, `specification.md`, `Dockerfile`, `docker-compose.yml`, `digitalocean-app.yaml`
- Creates deployment-ready artifacts

## Project-Specific Patterns

### Agent Implementation Pattern
```python
# Each agent follows this structure:
class MyAgent:
    def __init__(self):
        self.agent = create_agent(tool_names=[], model_id=MODEL_NAME)
        self.role = "Role Name"
    
    def do_work(self, spec, feedback=None):
        prompt = f"""You are a {self.role}...\n{spec}\n{feedback or ''}"""
        response = self.agent.run(task=prompt)
        return {"role": self.role, "output": str(response)}
```

### Configuration Loading
- `config_loader.py` merges YAML template with prompt overrides
- `constants.py` validates environment variables at import time
- Errors raised as `ConfigurationError` (custom exception in `constants.py`)

### Output Organization
- Deliverables saved to `output/` directory via `save_deliverables()` in `dev_team.py`
- Files: `specification.txt`, `final_code.py`, `ux_feedback.txt`, `test_feedback.txt`, `summary.txt`
- For DeepAgent: nested project structure with `src/`, `tests/`, and deployment configs

## Integration Points

### Provider Selection (agent_manager.py)
- `initialize_provider()` validates and authenticates with Abacus or HuggingFace
- `create_agent()` instantiates CodeAgent with selected model and tools
- Tool loading via dynamic imports using `AVAILABLE_TOOLS` registry

### External Dependencies
- **smolagents**: Core agent/tool framework (CodeAgent, ToolCallingAgent, search tools)
- **PyYAML**: Requirement file parsing
- **python-dotenv**: Environment variable loading
- **huggingface-hub**: HF authentication and inference
- **Flask/Gradio**: Web UI options (SmolAgentX/)

## Important Conventions

### Paths & Directory Structure
- Root project: `/workspaces/AgentX`
- Agents module: `Agents/` (has `__init__.py`)
- Requirements (case-sensitive): `Requirements/` with fallback to `requirements/`
- Output: `output/` directory (created on demand)
- Markdown docs: `MD/` directory

### Error Handling
- Use `ConfigurationError` for setup issues (raised by constants validation)
- Wrap YAML file operations in try/except, return structured dicts
- Agent failures should raise `ConfigurationError` with descriptive messages

### Feedback Format
- UX/Test feedback is passed as string to Developer in subsequent iterations
- Manager evaluates feedback to decide if code meets requirements
- Decision logic: All agents "approve" or max iterations reached

## Testing & Verification
- `test_imports.py`: Validates module imports
- `test_system.py`: System-level checks
- `verify_setup.py`: Checks environment and dependencies
- Run via: `python test_imports.py` or `pytest`

## Common Tasks

### Adding a New Agent Type
1. Create `Agents/new_agent.py` with agent class
2. Import in `ManagerAgent` 
3. Add to `coordinate_development()` workflow
4. Update README.md

### Changing Model Provider
Set `INFERENCE_PROVIDER=abacus` or `INFERENCE_PROVIDER=huggingface` in `.env`, then set corresponding API key (`ABACUS_API_KEY` or `HF_TOKEN`).

### Extending with New Tools
1. Register in `AVAILABLE_TOOLS` dict in `constants.py`
2. Pass tool names to `create_agent(tool_names=[...])`
3. Tools must be instantiable or callable

## Debugging Notes
- Enable Python tracebacks: set errors to print full stack traces
- Check `.env` file exists and has required variables
- YAML parsing errors often from indentation; use `yaml.safe_load()` 
- Model API rate limits: Abacus has request limits; HF has token limits
- Path issues: Use `Path(__file__).parent` for relative imports, prefer absolute paths
