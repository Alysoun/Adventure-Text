import random
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_state import GameState
from player import Player
from command_parser import CommandParser
from items import Item
from entities import Entity

def stress_test(iterations=1000):
    errors = []
    game_state = GameState(Player())
    
    try:
        # Create saves directory if it doesn't exist
        os.makedirs('saves', exist_ok=True)
        
        # Test save/load
        for i in range(iterations):
            save_name = f"stress_test_{i}.json"
            game_state.save_system.save_game(game_state, save_name)
            game_state.save_system.load_game(game_state, save_name)
            os.remove(os.path.join('saves', save_name))
            
    except Exception as e:
        errors.append(f"Stress test failed: {str(e)}")
        
    return errors

if __name__ == '__main__':
    print("Running stress test...")
    errors = stress_test()
    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nNo errors found!") 