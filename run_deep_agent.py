#!/usr/bin/env python3
"""
Runner script for the DeepAgent system.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from pathlib import Path

# Try to import the main function
try:
    from Agents.deep_agent import main as deep_agent_main
except ImportError as e:
    print(f"Error importing deep_agent module: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error initializing the DeepAgent system: {e}")
    sys.exit(1)


def main():
    try:
        # Look for a YAML file in the Requirements directory
        requirements_dir = Path(__file__).parent / "Requirements"
        if not requirements_dir.exists():
            requirements_dir = Path(__file__).parent / "requirements"

        yaml_files = []
        if requirements_dir.exists():
            yaml_files = list(requirements_dir.glob("*.yaml")) + list(requirements_dir.glob("*.yml"))

        if len(sys.argv) > 1:
            # Use the provided file path
            yaml_file_path = sys.argv[1]
            if Path(yaml_file_path).exists():
                deep_agent_main(yaml_file_path)
            else:
                print(f"❌ File not found: {yaml_file_path}")
                return 1
        elif yaml_files:
            print("Available requirement files:")
            for idx, file in enumerate(yaml_files, 1):
                print(f"{idx}. {file.name}")

            try:
                choice = input(f"\nSelect a file (1-{len(yaml_files)}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    print("👋 Exiting.")
                    return 0
                elif choice.isdigit() and 1 <= int(choice) <= len(yaml_files):
                    selected_file = yaml_files[int(choice) - 1]
                    deep_agent_main(str(selected_file))
                else:
                    print("❌ Invalid choice.")
                    return 1
            except KeyboardInterrupt:
                print("\n👋 Operation cancelled.")
                return 0
        else:
            print("❌ Usage: python run_deep_agent.py <path_to_yaml_file>")
            print("Or place YAML files in the Requirements directory and run without arguments.")
            return 1

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())