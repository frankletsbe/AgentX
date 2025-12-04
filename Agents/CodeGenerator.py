import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import ConfigurationError
from agent_manager import initialize_huggingface, create_agent


def main() -> None:
    print("=" * 60)
    print("Python Code Generator Agent")
    print("=" * 60)
    
    try:
        user_input = input("\nDescribe the Python application you want to create: ").strip()
        
        if not user_input:
            print("❌ No input provided. Exiting.")
            return
        
        prompt = f"""You are a Python code generator. Generate complete, working Python code based on the user's request.

User Request: {user_input}

Requirements:
- Generate clean, well-documented Python code
- Include all necessary imports
- Add comments explaining key functionality
- Follow Python best practices and PEP 8 style guide
- Make the code production-ready and executable
- Include error handling where appropriate

Generate the complete Python code now."""

        print("\n" + "=" * 60)
        print("GENERATING CODE...")
        print("=" * 60)
        
        initialize_huggingface()
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
            if not filename.endswith('.py'):
                filename += '.py'
            
            with open(filename, 'w') as f:
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
        print("Please check your configuration and try again.")
        return


if __name__ == "__main__":
    main()
