#!/usr/bin/env python3
"""
Final verification script for the DeepAgent system.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

print("=" * 60)
print("DEEP AGENT SYSTEM - FINAL VERIFICATION")
print("=" * 60)

# Check that all required files exist
required_files = [
    "Agents/deep_agent.py",
    "run_deep_agent.py",
    "Agents/manager_agent.py",
    "constants.py",
    "agent_manager.py",
    ".env.example",
    "requirements.txt",
    "Requirements/todo-app.yaml"
]

print("\nChecking required files:")
all_files_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - MISSING")
        all_files_exist = False

if all_files_exist:
    print("\n✅ ALL REQUIRED FILES ARE PRESENT!")
else:
    print("\n❌ SOME FILES ARE MISSING!")

# Check that all required modules can be imported
print("\nChecking module imports:")
missing_dependencies = []

try:
    from Agents.deep_agent import DeepAgent
    print("  ✅ DeepAgent module")
except ImportError as e:
    print(f"  ❌ DeepAgent module: {e}")
    if "smolagents" in str(e):
        missing_dependencies.append("smolagents")

try:
    from agent_manager import initialize_provider
    print("  ✅ Agent manager")
except ImportError as e:
    print(f"  ❌ Agent manager: {e}")
    if "smolagents" in str(e):
        missing_dependencies.append("smolagents")

try:
    from constants import AI_MODEL_NAME, PLANNING_MODEL_NAME
    print("  ✅ Constants")
except ImportError as e:
    print(f"  ❌ Constants: {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)

if missing_dependencies:
    print(f"\n⚠️  MISSING DEPENDENCIES DETECTED!")
    print("Please install the required dependencies:")
    print("  pip install -r requirements.txt")
else:
    print("\n✅ ALL MODULES CAN BE IMPORTED!")
    print("\nTo run the DeepAgent system:")
    print("1. Set up your environment variables in .env")
    print("2. Run: python run_deep_agent.py Requirements/todo-app.yaml")
    print(f"  ❌ {file} - MISSING")
    all_files_exist = False

if all_files_exist:
    print("\n✅ ALL REQUIRED FILES ARE PRESENT!")
else:
    print("\n❌ SOME FILES ARE MISSING!")

# Check that all required modules can be imported
print("\nChecking module imports:")
try:
    from Agents.deep_agent import DeepAgent
    print("  ✅ DeepAgent module")
except ImportError as e:
    print(f"  ❌ DeepAgent module: {e}")

try:
    from agent_manager import initialize_provider
    print("  ✅ Agent manager")
except ImportError as e:
    print(f"  ❌ Agent manager: {e}")

try:
    from constants import AI_MODEL_NAME, PLANNING_MODEL_NAME
    print("  ✅ Constants")
except ImportError as e:
    print(f"  ❌ Constants: {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print("\nTo run the DeepAgent system:")
print("1. Set up your environment variables in .env")
print("2. Run: python run_deep_agent.py Requirements/todo-app.yaml")