import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any, List
import yaml
from pathlib import Path
from analyst_agent import AnalystAgent
from developer_agent import DeveloperAgent
from tester_agent import TesterAgent
from ux_agent import UXAgent


class ManagerAgent:
    def __init__(self):
        self.analyst = AnalystAgent()
        self.developer = DeveloperAgent()
        self.tester = TesterAgent()
        self.ux = UXAgent()
        self.max_iterations = 3
        # Ensure exact casing for Requirements folder
        self.requirements_dir = Path(__file__).parent.parent / "Requirements"
        
    def load_available_requirements(self) -> List[Dict[str, Any]]:
        requirements = []
        # Fallback to lowercase 'requirements' if 'Requirements' doesn't exist
        if not self.requirements_dir.exists():
             self.requirements_dir = Path(__file__).parent.parent / "requirements"

        if not self.requirements_dir.exists():
            print(f"[WARNING] Requirements directory not found: {self.requirements_dir}")
            return requirements

        yaml_files = list(self.requirements_dir.glob("*.yaml")) + list(self.requirements_dir.glob("*.yml"))

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    requirements.append({
                        'filename': yaml_file.name,
                        'filepath': yaml_file,
                        'data': data
                    })
            except Exception as e:
                print(f"[WARNING] Could not load {yaml_file.name}: {e}")

        return requirements

    def select_requirement(self) -> Dict[str, Any]:
        requirements = self.load_available_requirements()

        if not requirements:
            print("\n[ERROR] No requirement files found in the requirements folder.")
            return None

        print("\n" + "="*80)
        print("AVAILABLE REQUIREMENTS")
        print("="*80)

        for idx, req in enumerate(requirements, 1):
            data = req['data']
            print(f"\n{idx}. {req['filename']}")
            if 'role' in data:
                print(f"   Role: {data['role'][:80]}...")
            if 'task' in data:
                task_preview = str(data['task']).strip()[:100].replace('\n', ' ')
                print(f"   Task: {task_preview}...")
            if 'requirements' in data:
                req_preview = str(data['requirements'])[:100].replace('\n', ' ')
                print(f"   Requirements: {req_preview}...")

        print("\n" + "="*80)

        while True:
            try:
                choice = input(f"\nSelect a requirement (1-{len(requirements)}) or 'q' to quit: ").strip()

                if choice.lower() == 'q':
                    return None

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(requirements):
                    selected = requirements[choice_idx]

                    output_folder_name = Path(selected['filename']).stem
                    selected['output_folder'] = output_folder_name

                    print(f"\n[MANAGER] Selected: {selected['filename']}")
                    print(f"[MANAGER] Output folder: {output_folder_name}/")
                    return selected
                else:
                    print(f"[ERROR] Please enter a number between 1 and {len(requirements)}")
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number or 'q' to quit.")
            except KeyboardInterrupt:
                print("\n[MANAGER] Selection cancelled.")
                return None

    def coordinate_development(self, user_requirement: str = None, requirement_data: Dict[str, Any] = None) -> Dict[str, Any]:
        print("\n" + "="*80)
        print("DEVELOPMENT TEAM WORKFLOW")
        print("="*80)

        output_folder = None
        full_context = ""

        if requirement_data:
            print(f"\n[MANAGER] Using requirement from: {requirement_data.get('filename', 'YAML file')}")
            data = requirement_data.get('data', {})

            output_folder = requirement_data.get('output_folder')
            if output_folder:
                print(f"[MANAGER] Output will be saved to: {output_folder}/")

            # Combine all fields into the requirement string for the Analyst
            full_context = "FULL PROJECT REQUIREMENTS FROM YAML FILE:\n"
            if 'role' in data:
                full_context += f"ROLE:\n{data['role']}\n\n"
            if 'task' in data:
                user_requirement = data['task'].strip()
                full_context += f"TASK DESCRIPTION:\n{user_requirement}\n\n"
            if 'requirements' in data:
                reqs = data['requirements']
                full_context += f"DETAILED REQUIREMENTS:\n{reqs}\n\n"
            if 'input_format' in data:
                full_context += f"INPUT FORMAT:\n{data['input_format']}\n\n"
            if 'output_format' in data:
                full_context += f"OUTPUT FORMAT:\n{data['output_format']}\n\n"
            if 'tools_description' in data:
                full_context += f"TOOLS DESCRIPTION:\n{data['tools_description']}\n\n"

            # Use the combined context as the actual prompt, falling back to user_requirement if manual entry
            prompt_requirement = full_context if full_context else user_requirement

        else:
            prompt_requirement = user_requirement

        if not user_requirement:
            print("\n[ERROR] No requirement provided.")
            return None

        print("\n[MANAGER] Delegating to Business Analyst...")
        print("-"*80)
        # Pass the rich context to the analyst
        analyst_result = self.analyst.analyze_requirements(prompt_requirement)
        specification = analyst_result["specification"]
        print(f"\n[ANALYST] Specification created:")
        print(specification[:500] + "..." if len(specification) > 500 else specification)
        
        iteration = 1
        ux_feedback = ""
        test_feedback = ""
        final_code = None
        
        while iteration <= self.max_iterations:
            print(f"\n{'='*80}")
            print(f"ITERATION {iteration}/{self.max_iterations}")
            print("="*80)
            
            print("\n[MANAGER] Delegating to Developer...")
            print("-"*80)
            dev_result = self.developer.develop_code(
                specification=specification,
                ux_feedback=ux_feedback,
                test_feedback=test_feedback
            )
            code = dev_result["code"]
            print(f"\n[DEVELOPER] Code generated (Length: {len(code)} chars)")
            
            print("\n[MANAGER] Delegating to UX Designer for review...")
            print("-"*80)
            ux_result = self.ux.review_ux(code=code, specification=specification)
            ux_feedback = ux_result["feedback"]
            print(f"\n[UX DESIGNER] Feedback:")
            print(ux_feedback[:500] + "..." if len(ux_feedback) > 500 else ux_feedback)
            
            print("\n[MANAGER] Delegating to QA Tester for review...")
            print("-"*80)
            test_result = self.tester.test_code(code=code, specification=specification)
            test_feedback = test_result["feedback"]
            print(f"\n[TESTER] Feedback:")
            print(test_feedback[:500] + "..." if len(test_feedback) > 500 else test_feedback)
            
            if self._is_feedback_positive(ux_feedback, test_feedback):
                print(f"\n[MANAGER] ✓ Code approved by team after {iteration} iteration(s)!")
                final_code = code
                break
            else:
                print(f"\n[MANAGER] Issues found. Requesting developer to address feedback...")
                
            iteration += 1
        
        if iteration > self.max_iterations:
            print(f"\n[MANAGER] Maximum iterations reached. Using latest version.")
            final_code = final_code or code

        return {
            "requirement": user_requirement,
            "specification": specification,
            "final_code": final_code,
            "ux_feedback": ux_feedback,
            "test_feedback": test_feedback,
            "iterations": iteration - 1 if iteration <= self.max_iterations else self.max_iterations,
            "output_folder": output_folder
        }
    
    def _is_feedback_positive(self, ux_feedback: str, test_feedback: str) -> bool:
        """
        Determines if the feedback indicates the code is ready.
        Improved logic to avoid false negatives on phrases like 'no issues found'.
        """
        combined = (ux_feedback + "\n" + test_feedback).lower()
        
        # Immediate disqualifiers (Strong negative signals)
        blockers = ["critical error", "syntax error", "fatal", "not working", "code is incomplete"]
        for b in blockers:
            if b in combined:
                return False

        # Positive indicators that suggest approval
        approvals = ["approved", "looks good", "no issues found", "passes all", "excellent", "ready for production"]
        
        # Count approvals
        approval_score = sum(1 for indicator in approvals if indicator in combined)
        
        # If we have strong approvals and no critical blockers, we are good.
        # We can also check if the word "issue" appears ONLY in the context of "no issues"
        
        if approval_score >= 1:
            return True
            
        # Fallback: if it's just 'issues' generic check (legacy logic but safer)
        # If "issue" is present, we check if it is preceded by "no "
        if "issue" in combined and "no issues" not in combined:
            return False
            
        return True