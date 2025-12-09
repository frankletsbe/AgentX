import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from constants import ConfigurationError, AI_MODEL_NAME, PLANNING_MODEL_NAME
from agent_manager import initialize_provider, create_agent


class DeepAgent:
    """Implementation of the DeepAgent prompt requirements for turning YAML requirements into complete Python applications."""
    
    def __init__(self):
        self.project_name = ""
        self.requirements_data = {}
        self.specification = ""
        self.code = ""
        self.tests = ""
        self.documentation = ""
        self.deployment_artifacts = {}
        
    def process_yaml_requirements(self, yaml_file_path: str) -> Dict[str, Any]:
        """
        Process a YAML requirements file and extract all necessary information.
        
        Args:
            yaml_file_path: Path to the YAML requirements file
            
        Returns:
            Dictionary containing parsed requirements data
        """
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            self.project_name = Path(yaml_file_path).stem
            self.requirements_data = data
            
            return {
                "project_name": self.project_name,
                "data": data
            }
        except Exception as e:
            raise ConfigurationError(f"Failed to process YAML requirements file: {e}")
    
    def analyze_requirements(self) -> str:
        """
        Analyst Agent: Analyze requirements and create detailed specification.
        
        Returns:
            Detailed specification document
        """
        print("[ANALYST] Analyzing requirements...")
        
        # Create a prompt for the analyst agent
        prompt = f"""You are a Business Analyst on a software development team.

USER REQUIREMENTS FROM YAML FILE:
{yaml.dump(self.requirements_data, default_flow_style=False)}

Your task is to analyze these requirements and create a detailed specification document that includes:

1. FUNCTIONAL REQUIREMENTS:
   - Core features and functionality based on the YAML requirements
   - User stories derived from the requirements
   - Acceptance criteria for each feature

2. NON-FUNCTIONAL REQUIREMENTS:
   - Performance expectations
   - Security considerations
   - Scalability needs

3. TECHNICAL CONSIDERATIONS:
   - Recommended technology stack suitable for the requirements
   - Architecture suggestions
   - Data models needed

4. USER INTERFACE REQUIREMENTS:
   - Key screens/pages needed (if applicable)
   - User flow
   - Input/output requirements

5. TESTING REQUIREMENTS:
   - Test scenarios
   - Edge cases to consider
   - Validation rules

Provide a comprehensive specification document in a structured format that a developer can use to implement the solution."""

        try:
            # Use the planning model for analysis
            from constants import PLANNING_MODEL_NAME
            analyst_agent = create_agent(tool_names=[], model_id=PLANNING_MODEL_NAME)
            response = analyst_agent.run(task=prompt)
            self.specification = str(response)
            return self.specification
        except Exception as e:
            raise ConfigurationError(f"Failed to analyze requirements: {e}")
    
    def design_ux(self) -> str:
        """
        UX Agent: Design user interaction model.
        
        Returns:
            UX design specification
        """
        print("[UX DESIGNER] Designing user experience...")
        
        prompt = f"""You are a UX Designer on a software development team.

SPECIFICATION:
{self.specification}

Based on this specification, design the user interaction model:

1. USER INTERACTION MODEL:
   - Determine if this is a CLI, API, web UI, or other interface
   - Define user flows
   - Specify endpoints/screens
   - Define error messages and validations

2. WIREFRAMES OR ENDPOINT SPECS:
   - Create simple textual descriptions of interfaces
   - Define user journeys
   - Specify input/output formats

Ensure the design is usable and clear for end users."""

        try:
            # Use the planning model for UX design
            from constants import PLANNING_MODEL_NAME
            ux_agent = create_agent(tool_names=[], model_id=PLANNING_MODEL_NAME)
            response = ux_agent.run(task=prompt)
            return str(response)
        except Exception as e:
            raise ConfigurationError(f"Failed to design UX: {e}")
    
    def develop_application(self, ux_design: str) -> str:
        """
        Developer Agent: Implement the Python application.
        
        Args:
            ux_design: UX design specification
            
        Returns:
            Generated Python code
        """
        print("[DEVELOPER] Developing application...")
        
        prompt = f"""You are a Software Developer on a development team.

SPECIFICATION:
{self.specification}

UX DESIGN:
{ux_design}

Your task is to implement a complete Python application that satisfies these requirements.

Requirements:
- Write clean, well-documented Python code following PEP 8 standards
- Include all necessary imports
- Follow Python best practices
- Add comprehensive error handling
- Include docstrings for all functions/classes
- Make the code modular and maintainable
- Create a complete, executable application with proper project structure
- Include a main entry point

Provide the complete implementation with all necessary files organized in a proper directory structure."""

        try:
            # Use the coding model for development
            from constants import AI_MODEL_NAME
            dev_agent = create_agent(tool_names=[], model_id=AI_MODEL_NAME)
            response = dev_agent.run(task=prompt)
            self.code = str(response)
            return self.code
        except Exception as e:
            raise ConfigurationError(f"Failed to develop application: {e}")
    
    def write_tests(self) -> str:
        """
        Tester Agent: Write automated tests.
        
        Returns:
            Generated test code
        """
        print("[TESTER] Writing automated tests...")
        
        prompt = f"""You are a QA Tester on a development team.

SPECIFICATION:
{self.specification}

CODE TO TEST:
{self.code}

Your task is to write comprehensive automated tests in Python using pytest:

Requirements:
- Write tests that cover main happy paths
- Include tests for important edge cases
- Use pytest framework
- Organize tests in a proper directory structure
- Include instructions for running the tests
- Document any risks or uncovered areas

Provide complete test files that can be executed with pytest."""

        try:
            # Use the coding model for testing
            from constants import AI_MODEL_NAME
            test_agent = create_agent(tool_names=[], model_id=AI_MODEL_NAME)
            response = test_agent.run(task=prompt)
            self.tests = str(response)
            return self.tests
        except Exception as e:
            raise ConfigurationError(f"Failed to write tests: {e}")
    
    def prepare_deployment(self) -> Dict[str, str]:
        """
        DevOps Agent: Prepare deployment artifacts for DigitalOcean.
        
        Returns:
            Dictionary of deployment artifacts
        """
        print("[DEVOPS] Preparing deployment artifacts...")
        
        prompt = f"""You are a DevOps Engineer preparing deployment artifacts for DigitalOcean.

SPECIFICATION:
{self.specification}

APPLICATION CODE:
{self.code}

Your task is to prepare all necessary deployment artifacts for DigitalOcean:

1. CONTAINERIZATION ARTIFACTS:
   - Create a Dockerfile for containerizing the application
   - Create a docker-compose.yml file if applicable

2. DEPLOYMENT CONFIGURATION:
   - Create any necessary configuration files for DigitalOcean deployment
   - Specify environment variables needed
   - Define ports and networking requirements

3. DEPLOYMENT INSTRUCTIONS:
   - Provide step-by-step instructions for deploying on DigitalOcean
   - Include options for App Platform, Droplets, or other DigitalOcean services
   - Specify build steps and runtime requirements

Provide all necessary files and documentation for deployment."""

        try:
            # Use the planning model for DevOps
            from constants import PLANNING_MODEL_NAME
            devops_agent = create_agent(tool_names=[], model_id=PLANNING_MODEL_NAME)
            response = devops_agent.run(task=prompt)
            
            # For now, we'll store the response as documentation
            # In a more sophisticated implementation, we would parse out the actual files
            self.deployment_artifacts["documentation"] = str(response)
            return self.deployment_artifacts
        except Exception as e:
            raise ConfigurationError(f"Failed to prepare deployment: {e}")
    
    def review_as_end_user(self) -> str:
        """
        End-User Agent: Review system from user perspective.
        
        Returns:
            End-user review feedback
        """
        print("[END-USER] Reviewing from user perspective...")
        
        prompt = f"""You are an End-User reviewing a software system.

ORIGINAL REQUIREMENTS FROM YAML:
{yaml.dump(self.requirements_data, default_flow_style=False)}

SPECIFICATION:
{self.specification}

APPLICATION CODE:
{self.code}

Your task is to review the system from a user's perspective:

1. VALIDATE REQUIREMENTS MATCH:
   - Check if functionality matches the original YAML requirements
   - Verify all acceptance criteria are addressed

2. USABILITY ASSESSMENT:
   - Evaluate if the UX flows make sense
   - Check if functionality matches typical user expectations

3. IMPROVEMENT SUGGESTIONS:
   - Suggest final minor improvements or clarifications
   - Identify any gaps between requirements and implementation

Provide feedback on how well the solution meets the user's needs."""

        try:
            # Use the planning model for end-user review
            from constants import PLANNING_MODEL_NAME
            enduser_agent = create_agent(tool_names=[], model_id=PLANNING_MODEL_NAME)
            response = enduser_agent.run(task=prompt)
            return str(response)
        except Exception as e:
            raise ConfigurationError(f"Failed to review as end-user: {e}")
    
    def generate_documentation(self) -> str:
        """
        Generate technical documentation.
        
        Returns:
            Technical documentation
        """
        print("[DOCUMENTATION] Generating technical documentation...")
        
        prompt = f"""You are a Technical Writer creating documentation for a software project.

SPECIFICATION:
{self.specification}

APPLICATION CODE:
{self.code}

TESTS:
{self.tests}

DEPLOYMENT INFORMATION:
{self.deployment_artifacts.get('documentation', 'No deployment information available')}

Create comprehensive technical documentation including:

1. PROJECT OVERVIEW:
   - Summary from the YAML requirements
   - Architecture summary and main components

2. SETUP INSTRUCTIONS:
   - How to set up and run locally
   - Prerequisites and dependencies

3. USAGE GUIDE:
   - How to use the application
   - Examples of key functionality

4. TESTING:
   - How to run the test suite
   - Explanation of test coverage

5. DEPLOYMENT:
   - How to build and deploy on DigitalOcean
   - Step-by-step deployment procedure

Write in a clear, technical tone suitable for developers who will maintain this code."""

        try:
            # Use the planning model for documentation
            from constants import PLANNING_MODEL_NAME
            doc_agent = create_agent(tool_names=[], model_id=PLANNING_MODEL_NAME)
            response = doc_agent.run(task=prompt)
            self.documentation = str(response)
            return self.documentation
        except Exception as e:
            raise ConfigurationError(f"Failed to generate documentation: {e}")
    
    def save_project(self, output_dir: Optional[str] = None) -> str:
        """
        Save all project artifacts to a structured directory.
        
        Args:
            output_dir: Optional output directory name (defaults to project name)
            
        Returns:
            Path to the created project directory
        """
        if not output_dir:
            output_dir = self.project_name
            
        project_path = Path(output_dir)
        project_path.mkdir(exist_ok=True)
        
        # Create standard directory structure
        src_path = project_path / "src"
        tests_path = project_path / "tests"
        src_path.mkdir(exist_ok=True)
        tests_path.mkdir(exist_ok=True)
        
        # Save specification
        with open(project_path / "specification.md", "w", encoding="utf-8") as f:
            f.write("# Project Specification\n\n")
            f.write(self.specification)
        
        # Save main application code
        self._save_code_files(src_path, self.code)
        
        # Save tests
        self._save_test_files(tests_path, self.tests)
        
        # Save documentation
        with open(project_path / "README.md", "w", encoding="utf-8") as f:
            f.write(self.documentation)
        
        # Create standard files
        self._create_standard_files(project_path)
        
        # Create deployment artifacts
        self._create_deployment_artifacts(project_path)
        
        print(f"\n✅ Project saved to '{project_path}/'")
        return str(project_path)
    
    def _save_code_files(self, src_path: Path, code_content: str) -> None:
        """Save code files, attempting to parse them from the response."""
        # Simple extraction of code blocks
        if "```python" in code_content:
            # Extract all Python code blocks
            import re
            code_blocks = re.findall(r"```python\s*(.*?)\s*```", code_content, re.DOTALL)
            
            if code_blocks:
                # Save main application
                with open(src_path / "main.py", "w", encoding="utf-8") as f:
                    f.write(code_blocks[0])
                
                # Save additional files if they exist
                for i, block in enumerate(code_blocks[1:], 1):
                    with open(src_path / f"module_{i}.py", "w", encoding="utf-8") as f:
                        f.write(block)
            else:
                # Save entire content if no code blocks found
                with open(src_path / "main.py", "w", encoding="utf-8") as f:
                    f.write(code_content)
        else:
            # Save entire content
            with open(src_path / "main.py", "w", encoding="utf-8") as f:
                f.write(code_content)
    
    def _save_test_files(self, tests_path: Path, test_content: str) -> None:
        """Save test files, attempting to parse them from the response."""
        # Simple extraction of test code blocks
        if "```python" in test_content:
            import re
            code_blocks = re.findall(r"```python\s*(.*?)\s*```", test_content, re.DOTALL)
            
            if code_blocks:
                # Save main test file
                with open(tests_path / "test_main.py", "w", encoding="utf-8") as f:
                    f.write(code_blocks[0])
                
                # Save additional test files if they exist
                for i, block in enumerate(code_blocks[1:], 1):
                    with open(tests_path / f"test_module_{i}.py", "w", encoding="utf-8") as f:
                        f.write(block)
            else:
                # Save entire content if no code blocks found
                with open(tests_path / "test_main.py", "w", encoding="utf-8") as f:
                    f.write(test_content)
        else:
            # Save entire content
            with open(tests_path / "test_main.py", "w", encoding="utf-8") as f:
                f.write(test_content)
    
    def _create_standard_files(self, project_path: Path) -> None:
        """Create standard project files."""
        # Create requirements.txt
        requirements_content = """# Auto-generated requirements
# Please update with actual dependencies
flask>=2.0.0
pytest>=6.0.0
"""
        with open(project_path / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements_content)
        
        # Create .gitignore
        gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environments
.env
.venv
venv/
ENV/
env/
"""
        with open(project_path / ".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
    
    def _create_deployment_artifacts(self, project_path: Path) -> None:
        """Create deployment artifacts for DigitalOcean."""
        # Create a basic Dockerfile
        dockerfile_content = """# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Expose port (adjust as needed)
EXPOSE 8000

# Run the application
CMD ["python", "src/main.py"]
"""
        with open(project_path / "Dockerfile", "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
        
        # Create docker-compose.yml
        compose_content = f"""version: '3.8'

services:
  {self.project_name}:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
    environment:
      - PYTHONPATH=/app
"""
        with open(project_path / "docker-compose.yml", "w", encoding="utf-8") as f:
            f.write(compose_content)
        
        # Create digitalocean.yml for App Platform (if needed)
        do_app_content = f"""name: {self.project_name}
region: nyc
services:
- name: {self.project_name}
  git:
    repo_clone_url: https://github.com/yourusername/{self.project_name}.git
    branch: main
  envs:
  - key: PYTHONPATH
    value: /app
  - key: FLASK_ENV
    value: production
  run_command: python src/main.py
  instance_size_slug: professional-xs
  instance_count: 1
  http_port: 8000
  routes:
  - path: /
"""
        with open(project_path / "digitalocean-app.yaml", "w", encoding="utf-8") as f:
            f.write(do_app_content)


def main(yaml_file_path: str) -> None:
    """Main entry point for the DeepAgent."""
    print("=" * 80)
    print("DEEP AGENT - YAML to Python Application Generator")
    print("=" * 80)
    
    try:
        # Initialize provider
        initialize_provider()
        
        # Create DeepAgent instance
        agent = DeepAgent()
        
        # Process YAML requirements
        print(f"\n[MANAGER] Processing requirements from: {yaml_file_path}")
        requirements_info = agent.process_yaml_requirements(yaml_file_path)
        print(f"[MANAGER] Project name: {requirements_info['project_name']}")
        
        # Phase 1: Understand & Analyze
        print("\n" + "-" * 80)
        print("PHASE 1: UNDERSTAND & ANALYZE")
        print("-" * 80)
        specification = agent.analyze_requirements()
        print("[MANAGER] Specification created")
        
        # Phase 2: Design UX & Architecture
        print("\n" + "-" * 80)
        print("PHASE 2: DESIGN UX & ARCHITECTURE")
        print("-" * 80)
        ux_design = agent.design_ux()
        print("[MANAGER] UX design completed")
        
        # Phase 3: Implement
        print("\n" + "-" * 80)
        print("PHASE 3: IMPLEMENT APPLICATION")
        print("-" * 80)
        code = agent.develop_application(ux_design)
        print("[MANAGER] Application development completed")
        
        # Phase 4: Test
        print("\n" + "-" * 80)
        print("PHASE 4: WRITE AUTOMATED TESTS")
        print("-" * 80)
        tests = agent.write_tests()
        print("[MANAGER] Automated tests written")
        
        # Phase 5: Deployability
        print("\n" + "-" * 80)
        print("PHASE 5: PREPARE DEPLOYMENT ARTIFACTS")
        print("-" * 80)
        deployment = agent.prepare_deployment()
        print("[MANAGER] Deployment artifacts prepared")
        
        # Phase 6: End-User Review
        print("\n" + "-" * 80)
        print("PHASE 6: END-USER REVIEW")
        print("-" * 80)
        end_user_review = agent.review_as_end_user()
        print("[MANAGER] End-user review completed")
        
        # Phase 7: Documentation
        print("\n" + "-" * 80)
        print("PHASE 7: GENERATE DOCUMENTATION")
        print("-" * 80)
        documentation = agent.generate_documentation()
        print("[MANAGER] Technical documentation generated")
        
        # Phase 8: Finalize and Save
        print("\n" + "-" * 80)
        print("PHASE 8: FINALIZE AND SAVE PROJECT")
        print("-" * 80)
        project_path = agent.save_project()
        
        print("\n" + "=" * 80)
        print("PROJECT GENERATION COMPLETE")
        print("=" * 80)
        print(f"Project saved to: {project_path}")
        print("Generated artifacts:")
        print("  - src/: Source code")
        print("  - tests/: Test files")
        print("  - specification.md: Detailed specification")
        print("  - README.md: Technical documentation")
        print("  - requirements.txt: Python dependencies")
        print("  - Dockerfile: Containerization configuration")
        print("  - docker-compose.yml: Multi-container configuration")
        print("  - digitalocean-app.yaml: DigitalOcean App Platform config")
        
    except ConfigurationError as e:
        print(f"\n❌ Configuration Error: {e}")
        return
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    # If run directly, look for a YAML file in the Requirements directory
    requirements_dir = Path(__file__).parent.parent / "Requirements"
    if not requirements_dir.exists():
        requirements_dir = Path(__file__).parent.parent / "requirements"
    
    yaml_files = []
    if requirements_dir.exists():
        yaml_files = list(requirements_dir.glob("*.yaml")) + list(requirements_dir.glob("*.yml"))
    
    if yaml_files:
        print("Available requirement files:")
        for idx, file in enumerate(yaml_files, 1):
            print(f"{idx}. {file.name}")
        
        try:
            choice = input(f"\nSelect a file (1-{len(yaml_files)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(yaml_files):
                selected_file = yaml_files[int(choice) - 1]
                main(str(selected_file))
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
    else:
        print("No YAML requirement files found in Requirements directory.")