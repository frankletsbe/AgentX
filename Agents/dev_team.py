import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import ConfigurationError
from agent_manager import initialize_huggingface
from manager_agent import ManagerAgent


def save_deliverables(result: dict, output_dir: str = "output") -> None:
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/specification.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("SPECIFICATION DOCUMENT\n")
        f.write("="*80 + "\n\n")
        f.write(result["specification"])
    
    with open(f"{output_dir}/final_code.py", "w", encoding="utf-8") as f:
        f.write(result["final_code"])
    
    with open(f"{output_dir}/ux_feedback.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("UX DESIGNER FEEDBACK\n")
        f.write("="*80 + "\n\n")
        f.write(result["ux_feedback"])
    
    with open(f"{output_dir}/test_feedback.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("QA TESTER FEEDBACK\n")
        f.write("="*80 + "\n\n")
        f.write(result["test_feedback"])
    
    with open(f"{output_dir}/summary.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("DEVELOPMENT SUMMARY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Original Requirement:\n{result['requirement']}\n\n")
        f.write(f"Iterations Completed: {result['iterations']}\n\n")
        f.write("Deliverables:\n")
        f.write("- specification.txt: Detailed specification document\n")
        f.write("- final_code.py: Final application code\n")
        f.write("- ux_feedback.txt: UX designer's feedback\n")
        f.write("- test_feedback.txt: QA tester's feedback\n")
    
    print(f"\n✓ All deliverables saved to '{output_dir}/' directory")


def main() -> None:
    print("="*80)
    print("AI DEVELOPMENT TEAM")
    print("="*80)
    print("\nTeam Members:")
    print("  - Business Analyst: Analyzes requirements and creates specifications")
    print("  - Software Developer: Writes code based on specifications")
    print("  - UX Designer: Reviews user experience and interface")
    print("  - QA Tester: Tests code and provides feedback")
    print("  - Manager: Coordinates the team workflow")
    print("="*80)

    try:
        print("\n[MANAGER] Initializing development team...")
        initialize_huggingface()

        manager = ManagerAgent()

        print("\nHow would you like to provide requirements?")
        print("1. Select from existing requirement files (YAML)")
        print("2. Enter requirement manually")

        choice = input("\nEnter your choice (1 or 2): ").strip()

        user_requirement = None
        requirement_data = None

        if choice == '1':
            requirement_data = manager.select_requirement()
            if not requirement_data:
                print("\n[MANAGER] No requirement selected. Exiting.")
                return
        elif choice == '2':
            user_requirement = input("\nDescribe the application you want to build: ").strip()
            if not user_requirement:
                print("❌ No requirement provided. Exiting.")
                return
        else:
            print("❌ Invalid choice. Exiting.")
            return

        result = manager.coordinate_development(user_requirement, requirement_data)

        if not result:
            print("\n[MANAGER] Development process failed. Exiting.")
            return

        print("\n" + "="*80)
        print("DEVELOPMENT COMPLETE")
        print("="*80)
        print(f"\nFinal Code:\n")
        print(result["final_code"])

        save_option = input("\n\nWould you like to save all deliverables? (y/n): ").strip().lower()
        if save_option == 'y':
            output_dir = input("Enter output directory name (default: 'output'): ").strip() or "output"
            save_deliverables(result, output_dir)

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


if __name__ == "__main__":
    main()
