# AI Development Team

A multi-agent system that simulates a complete software development team.

## Team Members

- **Business Analyst**: Analyzes user requirements and creates detailed specifications
- **Software Developer**: Writes production-ready code based on specifications
- **UX Designer**: Reviews user experience and interface design
- **QA Tester**: Tests code and provides feedback on bugs and improvements
- **Manager**: Coordinates the team workflow and manages iterations

## Workflow

1. **Requirements Analysis**: The analyst gathers and documents requirements
2. **Development**: The developer writes code based on specifications
3. **UX Review**: The UX designer reviews the user experience
4. **Testing**: The QA tester reviews code quality and functionality
5. **Iteration**: If issues are found, the developer addresses feedback (up to 3 iterations)
6. **Delivery**: Final code and documentation are delivered

## Usage

```bash
python agents/dev_team.py
```

You'll be prompted to describe the application you want to build. The team will then:
- Create a detailed specification
- Develop the code
- Review UX and test the code
- Iterate based on feedback
- Deliver the final application

## Output

The system generates:
- `specification.txt`: Detailed requirements document
- `final_code.py`: Production-ready application code
- `ux_feedback.txt`: UX designer's review
- `test_feedback.txt`: QA tester's review
- `summary.txt`: Development summary

## Configuration

Requires environment variables in `.env`:
- `HF_TOKEN`: Hugging Face API token
- `MODEL_NAME`: LLM model to use (default: Qwen/Qwen2.5-Coder-32B-Instruct)
- `SEARCH_PROVIDER`: Provider for model inference (default: openai)

## Features

- **Collaborative Feedback Loop**: Agents provide feedback to each other
- **Iterative Development**: Up to 3 iterations to refine the code
- **Quality Assurance**: Multiple perspectives ensure quality output
- **Complete Documentation**: All artifacts are saved for review
