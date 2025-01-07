import unittest
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_suites import (run_comprehensive_tests, TestInventorySystem, 
                              TestCombatSystem, TestQuestSystem, TestWorldGeneration, 
                              TestSaveSystem, TestCharacterSystem, TestEntityGenerator,
                              TestItemGenerator, TestNoteGenerator)
from tests.stress_test import stress_test

def run_all_tests():
    print("=== Running Unit Tests ===")
    run_comprehensive_tests()
    
    print("\n=== Running Stress Tests ===")
    errors = stress_test(iterations=1000)
    if errors:
        print("\nStress Test Errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nStress Tests Passed!")
        
    print("\n=== Testing Complete ===")

def run_comprehensive_tests():
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestInventorySystem,
        TestCombatSystem,
        TestQuestSystem,
        TestWorldGeneration,
        TestSaveSystem,
        TestCharacterSystem,
        TestEntityGenerator,    # Add new test cases
        TestItemGenerator,
        TestNoteGenerator
    ]
    
    for test_case in test_cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_all_tests() 