from agent_manager import initialize_huggingface, create_agent
import inspect

# Check function signatures
print("initialize_huggingface signature:", inspect.signature(initialize_huggingface))
print("create_agent signature:", inspect.signature(create_agent))

# Should print:
# initialize_huggingface signature: () -> None
# create_agent signature: (tool_names: List[str]) -> ToolCallingAgent