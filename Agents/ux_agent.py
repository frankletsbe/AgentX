import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any
from agent_manager import create_agent
from constants import PLANNING_MODEL_NAME

class UXAgent:
    def __init__(self):
        # UX Designer uses the PLANNING model
        self.agent = create_agent(tool_names=[], model_id=PLANNING_MODEL_NAME)
        self.role = "UX Designer"
        
    def review_ux(self, code: str, specification: str) -> Dict[str, Any]:
        prompt = f"""You are a UX Designer on a development team.

SPECIFICATION:
{specification}

CODE TO REVIEW:
{code}

Your task is to review the user experience and interface design:

1. USER INTERFACE ANALYSIS:
   - Evaluate the user interface design
   - Check if UI is intuitive and user-friendly
   - Verify accessibility considerations
   - Review input/output presentation

2. USER FLOW:
   - Analyze the user journey through the application
   - Identify any confusing or unclear steps
   - Suggest improvements to user flow

3. USABILITY:
   - Check error messages are clear and helpful
   - Verify prompts and instructions are understandable
   - Evaluate feedback provided to users
   - Check for consistent terminology

4. ACCESSIBILITY:
   - Consider users with different abilities
   - Check for clear instructions
   - Verify error handling is user-friendly

5. DESIGN RECOMMENDATIONS:
   - Suggest UI/UX improvements

Provide constructive feedback to the developer."""

        response = self.agent.run(task=prompt)
        
        return {
            "role": self.role,
            "feedback": str(response)
        }