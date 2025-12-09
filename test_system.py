#!/usr/bin/env python3
"""
Simple test script to verify the DeepAgent system.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

print("Testing DeepAgent system...")

# Try to import the main modules
try:
    from Agents.deep_agent import DeepAgent
    print("✓ DeepAgent module imported successfully")
except ImportError as e:
    print(f"❌ Error importing DeepAgent module: {e}")
    sys.exit(1)

# Try to import agent manager
try:
    from agent_manager import initialize_provider
    print("✓ Agent manager imported successfully")
except ImportError as e:
    print(f"❌ Error importing agent manager: {e}")
    sys.exit(1)

# Try to import constants
try:
    from constants import AI_MODEL_NAME, PLANNING_MODEL_NAME
    print("✓ Constants imported successfully")
    print(f"  AI_MODEL_NAME: {AI_MODEL_NAME}")
    print(f"  PLANNING_MODEL_NAME: {PLANNING_MODEL_NAME}")
except ImportError as e:
    print(f"❌ Error importing constants: {e}")
    sys.exit(1)

print("\n✅ All modules imported successfully! The DeepAgent system is ready to use.")