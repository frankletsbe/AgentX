# Enhanced AI Development Team with DeepAgent Support

This folder contains an enhanced multi-agent system that simulates a complete software development team and fully supports the DeepAgent prompt requirements for turning YAML requirements files into complete Python applications with deployment artifacts.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - For Abacus provider, set `INFERENCE_PROVIDER=abacus` and `ABACUS_API_KEY=your_key_here`
   - For Hugging Face provider, set `INFERENCE_PROVIDER=huggingface` and `HF_TOKEN=your_token_here`

3. Place your YAML requirements files in the `Requirements/` directory

## Features

- **Full YAML Requirements Support**: Process YAML files as the single source of truth
- **Multi-Agent Collaboration**: Business Analyst, Developer, UX Designer, QA Tester, and Manager agents
- **Structured Project Output**: Generates complete project folders with proper naming conventions
- **Deployment Artifacts**: Creates Dockerfiles, docker-compose.yml, and DigitalOcean configurations
- **Comprehensive Documentation**: Generates README.md and technical documentation
- **Automated Testing**: Creates test suites with pytest
- **DigitalOcean Ready**: All artifacts needed for deployment to DigitalOcean

## Usage

```bash
# Run with interactive file selection
python run_deep_agent.py

# Run with specific YAML file
python run_deep_agent.py path/to/requirements.yaml
```

## Agent Roles

- **Business Analyst**: Analyzes YAML requirements and creates detailed specifications
- **Software Developer**: Writes production-ready Python code
- **UX Designer**: Designs user interactions and reviews interfaces
- **QA Tester**: Writes automated tests and reviews code quality
- **Manager**: Coordinates the workflow and manages iterations
- **DevOps Engineer**: Prepares deployment artifacts for DigitalOcean
- **End-User**: Reviews the system from a user perspective
- **Technical Writer**: Generates comprehensive documentation

## Output Structure

Generated projects follow this structure:
```
<project-name>/
├── src/                 # Source code
├── tests/               # Test files
├── specification.md     # Detailed requirements specification
├── README.md            # Technical documentation
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization configuration
├── docker-compose.yml   # Multi-container configuration
├── digitalocean-app.yaml # DigitalOcean App Platform configuration
├── ux_feedback.md       # UX designer feedback
└── test_feedback.md     # QA tester feedback
```

## Agent Roles

- **Business Analyst**: Analyzes YAML requirements and creates detailed specifications
- **Software Developer**: Writes production-ready Python code
- **UX Designer**: Designs user interactions and reviews interfaces
- **QA Tester**: Writes automated tests and reviews code quality
- **Manager**: Coordinates the workflow and manages iterations
- **DevOps Engineer**: Prepares deployment artifacts for DigitalOcean
- **End-User**: Reviews the system from a user perspective
- **Technical Writer**: Generates comprehensive documentation

## Output Structure

Generated projects follow this structure:
```
<project-name>/
├── src/                 # Source code
├── tests/               # Test files
├── specification.md     # Detailed requirements specification
├── README.md            # Technical documentation
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization configuration
├── docker-compose.yml   # Multi-container configuration
├── digitalocean-app.yaml # DigitalOcean App Platform configuration
├── ux_feedback.md       # UX designer feedback
└── test_feedback.md     # QA tester feedback
```