import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any
from agent_manager import CustomInferenceClientModel
from constants import MODEL_NAME, SEARCH_PROVIDER


class DeveloperAgent:
    def __init__(self):
        client = CustomInferenceClientModel(MODEL_NAME, provider=SEARCH_PROVIDER)
        from smolagents import CodeAgent
        self.agent = CodeAgent(model=client, tools=[])
        self.role = "Software Developer"
        
    def develop_code(self, specification: str, ux_feedback: str = None, test_feedback: str = None) -> Dict[str, Any]:
        feedback_section = ""
        if ux_feedback:
            feedback_section += f"\n\nUX FEEDBACK TO ADDRESS:\n{ux_feedback}"
        if test_feedback:
            feedback_section += f"\n\nTEST FEEDBACK TO ADDRESS:\n{test_feedback}"
            
        prompt = f"""You are a Software Developer on a development team.

SPECIFICATION:
{specification}
{feedback_section}

Your task is to write complete, production-ready Python code that implements this specification.

Requirements:
- Write clean, well-documented code
- Include all necessary imports
- Follow Python best practices and PEP 8
- Add comprehensive error handling
- Include docstrings for all functions/classes
- Make the code modular and maintainable
- Address any feedback from UX and Testing teams
- Create a complete, executable application

Provide the complete Python code with clear file structure if multiple files are needed."""

        response = self.agent.run(task=prompt)
        
        return {
            "role": self.role,
            "code": str(response),
            "specification": specification
        }
