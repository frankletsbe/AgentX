import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_constants import ConfigurationError
from agent_manager import initialize_provider, create_agent
from manager_agent import ManagerAgent
import yaml
from pathlib import Path


def main() -> None:
    print("=" * 60)
    print("DeepAgent Code Generator")
    print("=" * 60)

    try:
        # Show available YAML files
        requirements_dir = Path(__file__).parent.parent / "Requirements"
        if not requirements_dir.exists():
            requirements_dir = Path(__file__).parent.parent / "requirements"

        yaml_files = []
        if requirements_dir.exists():
            yaml_files = list(requirements_dir.glob("*.yaml")) + list(requirements_dir.glob("*.yml"))

        if yaml_files:
            print("\nAvailable requirement files:")
            for idx, file in enumerate(yaml_files, 1):
                print(f"{idx}. {file.name}")

            print(f"{len(yaml_files) + 1}. Enter requirement manually")

            choice = input(f"\nSelect option (1-{len(yaml_files) + 1}): ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(yaml_files):
                selected_file = yaml_files[int(choice) - 1]
                print(f"\nUsing requirement file: {selected_file.name}")

                # Load the YAML file
                with open(selected_file, 'r', encoding='utf-8') as f:
                    requirement_data = yaml.safe_load(f)

                # Use the dev team workflow
                initialize_provider()
                manager = ManagerAgent()
                result = manager.coordinate_development(requirement_data=requirement_data)

                if result and result.get("final_code"):
                    project_name = selected_file.stem
                    save_project_artifacts(result, project_name)
                return
            elif choice == str(len(yaml_files) + 1):
                # Manual input path
                pass
            else:
                print("Invalid choice. Exiting.")
                return

        # Manual input path (original functionality)
        user_input = input("\nDescribe the application you want to create: ").strip()

        if not user_input:
            print("❌ No input provided. Exiting.")
            return

        prompt = f"""You are a code generator. Generate complete, working code based on the user's request.

User Request: {user_input}

Requirements:
- Generate clean, well-documented code
- Include all necessary imports
- Add comments explaining key functionality
- Follow best practices
- Make the code production-ready and executable
- Include error handling where appropriate

Generate the complete code now."""

        print("\n" + "=" * 60)
        print("GENERATING CODE...")
        print("=" * 60)

        # Use generic provider initialization
        initialize_provider()

        # Use create_agent instead of Hardcoding HuggingFace
        agent = create_agent(["DuckDuckGoSearchTool"])

        print("\nProcessing your request...")
        print("-" * 60)
        response = agent.run(task=prompt)

        print("\n" + "=" * 60)
        print("GENERATED CODE:")
        print("=" * 60)
        print(response)

        save_option = input("\n\nWould you like to save this code to a file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = input("Enter filename (e.g., my_app.py): ").strip()
            if not filename:
                filename = "generated_app.py"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(response))
            print(f"✅ Code saved to {filename}")

    except ConfigurationError as e:
        print(f"\n❌ Configuration Error: {e}")
        return
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        return
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return


def save_project_artifacts(result: dict, project_name: str) -> None:
    """Save all project artifacts in a structured directory."""
    # Create project directory
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)

    # Create standard directory structure
    src_dir = project_dir / "src"
    tests_dir = project_dir / "tests"
    src_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)

    # Save specification
    with open(project_dir / "specification.md", "w", encoding="utf-8") as f:
        f.write("# Project Specification\n\n")
        f.write(result.get("specification", "No specification provided"))

    # Save main code
    code_content = result.get("final_code", "")
    if code_content:
        # Try to extract actual Python code from the response
        if "```python" in code_content:
            # Extract code between triple backticks
            start = code_content.find("```python") + 10
            end = code_content.find("```", start)
            if end > start:
                code_content = code_content[start:end].strip()

        with open(src_dir / "main.py", "w", encoding="utf-8") as f:
            f.write(code_content)

    # Save UX feedback
    with open(project_dir / "ux_feedback.md", "w", encoding="utf-8") as f:
        f.write("# UX Designer Feedback\n\n")
        f.write(result.get("ux_feedback", "No UX feedback provided"))

    # Save test feedback
    with open(project_dir / "test_feedback.md", "w", encoding="utf-8") as f:
        f.write("# QA Tester Feedback\n\n")
        f.write(result.get("test_feedback", "No test feedback provided"))

    # Create README.md
    create_readme(project_dir, project_name, result)

    # Create requirements.txt
    create_requirements_txt(project_dir)

    # Create Dockerfile for DigitalOcean deployment
    create_dockerfile(project_dir)

    # Create docker-compose.yml
    create_docker_compose(project_dir)

    # Create basic test structure
    create_test_structure(tests_dir)

    print(f"\n✅ Project artifacts saved to '{project_name}/' directory")
    print(f"\n📁 Project Structure:")
    print(f"   {project_name}/")
    print(f"   ├── src/")
    print(f"   │   └── main.py")
    print(f"   ├── tests/")
    print(f"   │   └── test_main.py")
    print(f"   ├── specification.md")
    print(f"   ├── README.md")
    print(f"   ├── requirements.txt")
    print(f"   ├── Dockerfile")
    print(f"   ├── docker-compose.yml")
    print(f"   ├── ux_feedback.md")
    print(f"   └── test_feedback.md")


def create_readme(project_dir: Path, project_name: str, result: dict) -> None:
    """Create a comprehensive README.md file."""
    readme_content = f"""# {project_name}

## Project Overview

{result.get('requirement', 'No requirement description available.')}

## Architecture Summary

This project was generated using an AI-powered development team consisting of:
- Business Analyst: Analyzes requirements and creates specifications
- Software Developer: Writes production-ready code
- UX Designer: Reviews user experience and interface design
- QA Tester: Tests code and provides feedback
- Manager: Coordinates the team workflow

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python src/main.py
```

## Running Tests

```bash
pytest tests/
```

## Deployment to DigitalOcean

### Option 1: Using Docker

1. Build the Docker image:
   ```bash
   docker build -t {project_name} .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 {project_name}
   ```

### Option 2: Deploy to DigitalOcean App Platform

1. Fork this repository to your GitHub account
2. Create a new app on DigitalOcean App Platform
3. Connect your GitHub repository
4. Configure the app to use the Dockerfile
5. Deploy!

### Option 3: Deploy to DigitalOcean Droplet

1. Create a new Ubuntu droplet
2. SSH into your droplet
3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```
4. Copy your project files to the droplet
5. Build and run the Docker container:
   ```bash
   docker build -t {project_name} .
   docker run -d -p 80:8000 {project_name}
   ```

## Project Structure

```
{project_name}/
├── src/                 # Source code
├── tests/               # Test files
├── specification.md     # Detailed project specification
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── README.md            # This file
├── ux_feedback.md       # UX designer feedback
└── test_feedback.md     # QA tester feedback
```

## Development Team Workflow

This project was developed through an iterative process:
1. Requirements analysis by Business Analyst
2. Code development by Software Developer
3. UX review by UX Designer
4. Testing by QA Tester
5. Iterative refinement based on feedback

"""

    with open(project_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)


def create_requirements_txt(project_dir: Path) -> None:
    """Create a requirements.txt file."""
    requirements_content = """flask==2.3.3
pytest==7.4.2
requests==2.31.0
python-dotenv==1.0.0
"""

    with open(project_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)


def create_dockerfile(project_dir: Path) -> None:
    """Create a Dockerfile for containerization."""
    dockerfile_content = """# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "src/main.py"]
"""

    with open(project_dir / "Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile_content)


def create_docker_compose(project_dir: Path) -> None:
    """Create a docker-compose.yml file."""
    compose_content = f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
    environment:
      - FLASK_ENV=development
"""

    with open(project_dir / "docker-compose.yml", "w", encoding="utf-8") as f:
        f.write(compose_content)


def create_test_structure(tests_dir: Path) -> None:
    """Create basic test structure."""
    test_content = """import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import your main module here
# from main import your_main_function

def test_example():
    \"\"\"Example test case.\"\"\"
    assert True

if __name__ == "__main__":
    pytest.main([__file__])
"""

    with open(tests_dir / "test_main.py", "w", encoding="utf-8") as f:
        f.write(test_content)


if __name__ == "__main__":
    main()