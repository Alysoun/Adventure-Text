import unittest
from game_state import GameState
from player import Player
from command_parser import CommandParser
from commands import *

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.player = Player()
        self.game_state = GameState(self.player)
        self.parser = CommandParser()
        
        # Initialize starting location
        start_location = self.game_state._generate_meadow()
        self.game_state.set_current_location(start_location)

    def test_basic_commands(self):
        """Test all basic commands work without crashing"""
        commands = [
            "look", "survey", "inventory", "help",
            "look north", "look south", "look east", "look west",
            "examine note", "status", "quests", "achievements"
        ]
        
        for cmd in commands:
            with self.subTest(command=cmd):
                command = self.parser.parse(cmd)
                self.assertIsNotNone(command, f"Command '{cmd}' not recognized")
                try:
                    command.execute(self.game_state)
                except Exception as e:
                    self.fail(f"Command '{cmd}' raised {type(e).__name__}: {str(e)}")

    def test_movement(self):
        """Test movement in all directions"""
        directions = ["north", "south", "east", "west"]
        for direction in directions:
            with self.subTest(direction=direction):
                cmd = self.parser.parse(f"go {direction}")
                try:
                    cmd.execute(self.game_state)
                except Exception as e:
                    self.fail(f"Movement '{direction}' raised {type(e).__name__}: {str(e)}")

    def test_combat(self):
        """Test combat mechanics"""
        # Add hostile entity
        wolf = self.game_state.entity_generator.generate_entity("wolf", "hostile")
        self.game_state.current_location.add_entity(wolf)
        
        cmd = self.parser.parse("attack wolf")
        try:
            cmd.execute(self.game_state)
        except Exception as e:
            self.fail(f"Combat raised {type(e).__name__}: {str(e)}")

    def test_item_interactions(self):
        """Test item-related commands"""
        # Add test item
        test_item = Item("test_sword", "A test sword", "weapon", damage_bonus=5)
        self.game_state.current_location.add_item(test_item)
        
        commands = [
            "take test_sword",
            "examine test_sword",
            "equip test_sword",
            "unequip test_sword",
            "drop test_sword"
        ]
        
        for cmd in commands:
            with self.subTest(command=cmd):
                command = self.parser.parse(cmd)
                try:
                    command.execute(self.game_state)
                except Exception as e:
                    self.fail(f"Command '{cmd}' raised {type(e).__name__}: {str(e)}")

    def test_quest_progression(self):
        """Test quest triggers and updates"""
        # Test cooking quest
        cmd = self.parser.parse("cook")
        try:
            cmd.execute(self.game_state)
            self.assertIn("made_camp", self.game_state.milestones)
        except Exception as e:
            self.fail(f"Quest progression raised {type(e).__name__}: {str(e)}")

class TestAchievements(unittest.TestCase):
    # Similar structure for testing achievements
    pass

class TestCombatSystem(unittest.TestCase):
    # Detailed combat system tests
    pass

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests() 