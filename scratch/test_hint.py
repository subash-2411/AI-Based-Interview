import sys
import os
import traceback

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.logic import get_coding_hint

try:
    print("Testing get_coding_hint...")
    hint = get_coding_hint("Two Sum", "Find two numbers that add to target", "def solution(nums, target): pass")
    with open("scratch/error.log", "w") as f:
        f.write("Success! Hint returned:\n")
        f.write(hint)
except Exception as e:
    with open("scratch/error.log", "w") as f:
        f.write("Exception occurred:\n")
        f.write(traceback.format_exc())
