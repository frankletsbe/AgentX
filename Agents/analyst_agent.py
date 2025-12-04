import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any
from agent_manager import create_agent, CustomInferenceClientModel
from constants import MODEL_NAME, SEARCH_PROVIDER


class AnalystAgent:
    def __init__(self):
        client = CustomInferenceClientModel(MODEL_NAME, provider=SEARCH_PROVIDER)
        from smolagents import CodeAgent
        self.agent = CodeAgent(model=client, tools=[])
        self.role = "Business Analyst"
        
    def analyze_requirements(self, user_requirement: str) -> Dict[str, Any]:
        prompt = f"""You are a Business Analyst on a software development team.

User Requirement: {user_requirement}

Your task is to analyze this requirement and create a detailed specification document that includes:

1. FUNCTIONAL REQUIREMENTS:
   - Core features and functionality
   - User stories
   - Acceptance criteria

2. NON-FUNCTIONAL REQUIREMENTS:
   - Performance expectations
   - Security considerations
   - Scalability needs

3. TECHNICAL CONSIDERATIONS:
   - Recommended technology stack
   - Architecture suggestions
   - Data models needed

4. USER INTERFACE REQUIREMENTS:
   - Key screens/pages needed
   - User flow
   - Input/output requirements

5. TESTING REQUIREMENTS:
   - Test scenarios
   - Edge cases to consider
   - Validation rules

Provide a comprehensive specification document in a structured format."""

        response = self.agent.run(task=prompt)
        
        return {
            "role": self.role,
            "specification": str(response),
            "original_requirement": user_requirement
        }
