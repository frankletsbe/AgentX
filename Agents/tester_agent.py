import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any
from agent_manager import create_agent
from constants import AI_MODEL_NAME

class TesterAgent:
    def __init__(self):
        # QA Tester uses the Coding/AI model (better at detailed code analysis)
        self.agent = create_agent(tool_names=[], model_id=AI_MODEL_NAME)
        self.role = "QA Tester"
        
    def test_code(self, code: str, specification: str) -> Dict[str, Any]:
        prompt = f"""You are a QA Tester on a development team.

SPECIFICATION:
{specification}

CODE TO TEST:
{code}

Your task is to thoroughly review and test this code:

1. CODE REVIEW:
   - Check if code meets all specification requirements
   - Verify error handling is comprehensive
   - Check for potential bugs or edge cases
   - Review code quality and best practices

2. TEST SCENARIOS:
   - Identify test cases that should be covered
   - List positive test scenarios
   - List negative test scenarios
   - Identify edge cases

3. SECURITY REVIEW:
   - Check for security vulnerabilities
   - Verify input validation
   - Check for potential injection attacks

4. PERFORMANCE CONSIDERATIONS:
   - Identify potential performance bottlenecks
   - Suggest optimizations if needed

5. FEEDBACK FOR DEVELOPER:
   - List any bugs found
   - Suggest improvements
   - Highlight missing functionality
   - Rate code quality (1-10)

Provide detailed testing feedback with specific issues and recommendations."""

        response = self.agent.run(task=prompt)
        
        return {
            "role": self.role,
            "feedback": str(response),
            "code_reviewed": code
        }