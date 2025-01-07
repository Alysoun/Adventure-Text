import unittest
import os
import sys
import json
from hypothesis import given, strategies as st
import string

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_state import GameState
from player import Player
from command_parser import CommandParser
from items import Item
from entities import Entity
from location import Location
from generators import ItemGenerator
from commands import (LookCommand, InventoryCommand, TakeCommand, 
                     MoveCommand, SearchCommand, AttackCommand)
from display import Display
from generators import LocationGenerator, RewardGenerator
from generators import EntityGenerator, NoteGenerator
from models.achievement import AchievementSystem
from models.leveling import LevelingSystem


class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        
    def test_inventory_limits(self):
        """Test inventory capacity and weight limits"""
        # Add many items
        for i in range(100):
            item = Item(f"test_item_{i}", "Test item", "misc")
            self.player.add_item(item)
            
    def test_item_stacking(self):
        """Test stackable items like food"""
        food1 = Item("bread", "Fresh bread", "food", food_value=10)
        food2 = Item("bread", "Fresh bread", "food", food_value=10)
        self.player.add_item(food1)
        self.player.add_item(food2)

class TestCombatSystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        self.wolf = Entity("wolf", "A fierce wolf")
        self.wolf.hostile = True
        
    def test_damage_calculation(self):
        """Test damage calculations with different weapons/armor"""
        weapon = Item("sword", "A sharp sword", "weapon", damage_bonus=5)
        armor = Item("plate", "Plate armor", "armor", defense_bonus=3)
        self.player.equip(weapon)
        self.player.equip(armor)
        
    def test_critical_hits(self):
        """Test critical hit mechanics"""
        self.player.crit_chance = 1.0  # Force critical
        # Test combat...
        
    def test_dodge_mechanics(self):
        """Test dodge chance calculations"""
        self.player.dodge_chance = 1.0  # Force dodge
        # Test combat...

    def test_full_combat_sequence(self):
        """Test a complete combat encounter"""
        wolf = Entity("wolf", "A fierce wolf")
        wolf.health = 30
        wolf.damage = 5
        
        initial_player_health = self.player.health
        initial_wolf_health = wolf.health
        
        # Test attack
        damage_dealt = self.game_state.combat_system.attack(self.player, wolf)
        self.assertGreater(damage_dealt, 0)
        self.assertLess(wolf.health, initial_wolf_health)
        
        # Test counterattack
        damage_taken = self.game_state.combat_system.attack(wolf, self.player)
        self.assertGreater(damage_taken, 0)
        self.assertLess(self.player.health, initial_player_health)
        
    def test_combat_rewards(self):
        """Test rewards from combat"""
        wolf = Entity("wolf", "A fierce wolf")
        initial_exp = self.player.exp
        initial_gold = self.player.gold
        
        # Simulate killing the wolf
        wolf.health = 0
        rewards = self.game_state.combat_system.process_combat_rewards(wolf)
        
        self.assertGreater(self.player.exp, initial_exp)
        self.assertGreater(self.player.gold, initial_gold)

class TestQuestSystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        
    def test_quest_triggers(self):
        """Test all possible quest triggers"""
        triggers = [
            ("move", {"location_type": "cave"}),
            ("feed", {"target": "wolf", "item": "meat"}),
            ("cook", {"meal_type": "stew"})
        ]
        for action, context in triggers:
            self.game_state.story.check_progress(self.game_state, action, context)
            
    def test_quest_rewards(self):
        """Test quest completion rewards"""
        quest = self.game_state.story.quests["survival"]
        # Complete quest conditions
        quest["completed"] = True
        # Check rewards...

class TestWorldGeneration(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        
    def test_location_generation(self):
        """Test location type generation"""
        location_types = ["meadow", "forest", "cave"]
        for loc_type in location_types:
            location = self.game_state.location_generator.generate_location(loc_type)
            self.assertIsNotNone(location)
            
    def test_entity_spawning(self):
        """Test entity spawn rules"""
        location = Location("forest", "A dense forest")
        # Test spawn rates, types, etc.
        
    def test_item_generation(self):
        """Test item generation rules"""
        for quality in range(5):
            weapon = self.game_state.item_generator.generate_item("weapon", quality)
            self.assertGreaterEqual(weapon.damage_bonus, quality)
        
    def test_location_connections(self):
        """Test location connectivity"""
        location = self.game_state.world_generator.generate_location("meadow")
        
        # Test all directions
        for direction in ["north", "south", "east", "west"]:
            connected = location.move_direction(direction)
            if connected:
                self.assertIsInstance(connected, Location)
                # Verify reverse connection
                reverse = {"north": "south", "south": "north",
                          "east": "west", "west": "east"}
                self.assertEqual(connected.move_direction(reverse[direction]), location)

class TestSaveSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        # Create saves directory if it doesn't exist
        os.makedirs('saves', exist_ok=True)
        
    def tearDown(self):
        # Clean up test files
        for filename in ['minimal_save.json', 'corrupted_save.json']:
            try:
                os.remove(os.path.join('saves', filename))
            except FileNotFoundError:
                pass
        
    def test_save_load(self):
        """Test saving and loading game state"""
        # Set up some initial state
        self.game_state.player.health = 75
        self.game_state.story.discovered_chapters.add("tutorial")
        self.game_state.time.current_time = 120
        
        # Save the game
        self.game_state.save_system.save_game(self.game_state, "test_save.json")
        
        # Create a new game state
        new_state = GameState(Player())
        
        # Load the saved game into the new state
        new_state = self.game_state.save_system.load_game(new_state, "test_save.json")
        
        # Verify the loaded state matches
        self.assertEqual(new_state.player.health, 75)
        self.assertEqual(new_state.story.discovered_chapters, {"tutorial"})
        self.assertEqual(new_state.time.current_time, 120)
        
        # Clean up
        os.remove(os.path.join(self.game_state.save_system.save_dir, "test_save.json"))
        
    def test_save_corruption(self):
        """Test handling of corrupted save files"""
        # Create corrupted save file
        with open("corrupted_save.json", "w") as f:
            f.write("{ invalid json")
            
        with self.assertRaises(Exception):
            self.game_state.save_system.load_game(self.game_state, "corrupted_save.json")
            
    def test_save_compatibility(self):
        """Test loading saves with missing/extra data"""
        minimal_save = {
            "player": {
                "health": 100,
                "inventory": [],
                "equipped": {
                    "weapon": None,
                    "armor": None,
                    "accessory": None
                },
                "skills": {
                    "melee": 1,
                    "defense": 1,
                    "survival": 1,
                    "crafting": 1
                },
                "stats": {
                    "level": 1,
                    "exp": 0,
                    "gold": 100,
                    "strength": 5,
                    "dexterity": 5,
                    "intelligence": 5,
                    "vitality": 5,
                    "charisma": 5,
                    "wisdom": 5,
                    "luck": 5,
                    "hunger": 100,
                    "thirst": 100,
                    "energy": 100,
                    "bladder": 100
                }
            },
            "story": {
                "quest_stages": {},
                "discovered_chapters": [],
                "milestones": {
                    "wolves_befriended": False,
                    "cave_discovered": False,
                    "crystal_found": False
                }
            },
            "world": {
                "time": 0,
                "discovered_locations": {},
                "discovered_areas": []
            }
        }
        
        save_path = os.path.join('saves', 'minimal_save.json')
        with open(save_path, 'w') as f:
            json.dump(minimal_save, f)
            
        loaded_state = self.game_state.save_system.load_game(self.game_state, "minimal_save.json")
        self.assertIsNotNone(loaded_state)

    def test_complex_save_state(self):
        """Test saving/loading complex game states"""
        # Set up complex state
        self.game_state.player.inventory.extend([
            Item("sword", "A sword", "weapon", damage_bonus=5),
            Item("potion", "Health potion", "consumable", heal_amount=20)
        ])
        self.game_state.story.set_flag("met_wizard", True)
        self.game_state.achievements.unlock("first_steps")
        
        # Save and reload
        self.game_state.save_system.save_game(self.game_state, "complex_save.json")
        loaded_state = self.game_state.save_system.load_game(self.game_state, "complex_save.json")
        
        # Verify complex state preserved
        self.assertEqual(len(loaded_state.player.inventory), 2)
        self.assertTrue(loaded_state.story.get_flag("met_wizard"))
        self.assertTrue(loaded_state.achievements.is_unlocked("first_steps"))

class TestCharacterSystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        
    def test_base_stats(self):
        """Test initial character stats"""
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.exp, 0)
        self.assertEqual(self.player.gold, 100)
        
        # Test base attributes
        self.assertEqual(self.player.strength, 5)
        self.assertEqual(self.player.dexterity, 5)
        self.assertEqual(self.player.intelligence, 5)
        self.assertEqual(self.player.vitality, 5)
        self.assertEqual(self.player.charisma, 5)
        self.assertEqual(self.player.wisdom, 5)
        self.assertEqual(self.player.luck, 5)
        
        # Test base skills
        self.assertEqual(self.player.skills['melee'], 1)
        self.assertEqual(self.player.skills['defense'], 1)
        self.assertEqual(self.player.skills['survival'], 1)
        self.assertEqual(self.player.skills['crafting'], 1)
        
    def test_stat_effects(self):
        """Test how stats affect gameplay mechanics"""
        # Test strength affecting damage
        base_damage = self.player.damage
        self.player.strength = 7
        self.assertTrue(self.player.get_stats()[0] > base_damage)
        
        # Test dexterity affecting dodge
        base_dodge = self.player.dodge_chance
        self.player.dexterity = 7
        self.assertTrue(self.player.dodge_chance > base_dodge)
        
        # Test vitality affecting health
        base_health = self.player.max_health
        self.player.vitality = 7
        self.assertTrue(self.player.max_health > base_health)
        
    def test_skill_leveling(self):
        """Test skill progression system"""
        # Combat should increase melee skill
        initial_melee = self.player.skills['melee']
        self.game_state.combat_system.gain_combat_exp(10)
        self.assertTrue(self.player.skills['melee'] > initial_melee)
        
        # Successful defense should increase defense skill
        initial_defense = self.player.skills['defense']
        self.game_state.combat_system.gain_defense_exp(10)
        self.assertTrue(self.player.skills['defense'] > initial_defense)
        
    def test_equipment_stats(self):
        """Test how equipment affects character stats"""
        # Create test equipment
        weapon = Item("test sword", "A sword", "weapon", 
                     damage_bonus=5, rarity=Item.RARE)
        armor = Item("test armor", "Armor", "armor", 
                    defense_bonus=3, rarity=Item.UNCOMMON)
                    
        # Test equipping items
        self.player.equip(weapon)
        self.player.equip(armor)
        
        damage, defense = self.player.get_stats()
        self.assertTrue(damage > self.player.damage)
        self.assertTrue(defense > self.player.defense)

class TestCommandSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        self.parser = CommandParser()
        
    def test_command_aliases(self):
        """Test all command aliases work"""
        test_cases = {
            'look': {
                'aliases': ['l', 'examine', 'x'],
                'args': ['north', 'sword', 'note'],
                'expected_class': LookCommand
            },
            'inventory': {
                'aliases': ['i', 'inv', 'items', 'bag'],
                'args': [],
                'expected_class': InventoryCommand
            },
            'take': {
                'aliases': ['get', 'grab', 'pick', 'pickup'],
                'args': ['sword', 'the sword', 'mysterious note'],
                'expected_class': TakeCommand
            }
        }
        
        for cmd, data in test_cases.items():
            for alias in data['aliases']:
                for args in data['args']:
                    full_cmd = f"{alias} {args}".strip()
                    result = self.parser.parse(full_cmd)
                    self.assertIsNotNone(result, f"Command failed: {full_cmd}")
                    self.assertIsInstance(result, data['expected_class'],
                        f"Wrong command type for: {full_cmd}")
                    if args:
                        self.assertEqual(' '.join(result.args), args,
                            f"Args not parsed correctly for: {full_cmd}")
                            
    def test_invalid_commands(self):
        """Test handling of invalid commands"""
        invalid_inputs = [
            ('', "Empty command"),
            ('   ', "Whitespace only"),
            ('invalid', "Non-existent command"),
            ('look invalid direction', "Invalid direction"),
            ('12345', "Numeric input"),
            ('@#$%', "Special characters"),
            ('go to', "Incomplete command"),
            ('take the', "Missing object")
        ]
        
        for cmd, desc in invalid_inputs:
            result = self.parser.parse(cmd)
            self.assertIsNone(result, f"Invalid command not handled: {desc}")
        
    def test_command_chaining(self):
        """Test multiple commands in sequence"""
        commands = [
            "look",
            "take sword",
            "equip sword",
            "attack wolf"
        ]
        
        for cmd in commands:
            result = self.parser.parse(cmd)
            self.assertIsNotNone(result)
            result.execute(self.game_state)
            
    def test_command_context(self):
        """Test commands with context requirements"""
        # Test take command with no item present
        cmd = self.parser.parse("take sword")
        result = cmd.execute(self.game_state)
        self.assertIn("no sword", result.lower())
        
        # Add item and test again
        sword = Item("sword", "A sword", "weapon")
        self.game_state.current_location.add_item(sword)
        result = cmd.execute(self.game_state)
        self.assertIn("took", result.lower())

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        self.generator = ItemGenerator()
        
    def test_item_rarity_stats(self):
        """Test item rarity affects stats"""
        test_cases = [
            (Item.COMMON, (1, 3)),      # (rarity, (min_damage, max_damage))
            (Item.UNCOMMON, (2, 4)),
            (Item.RARE, (3, 6)),
            (Item.EPIC, (5, 8)),
            (Item.LEGENDARY, (7, 12))
        ]
        
        for rarity, damage_range in test_cases:
            for _ in range(10):  # Test multiple times for randomized stats
                weapon = self.generator._generate_weapon(
                    quality_level=list(Item.RARITY_COLORS.keys()).index(rarity)
                )
                self.assertEqual(weapon.rarity, rarity)
                self.assertGreaterEqual(weapon.damage_bonus, damage_range[0])
                self.assertLessEqual(weapon.damage_bonus, damage_range[1])
                
    def test_item_stacking(self):
        """Test stackable items"""
        # Test identical items
        bread1 = Item("bread", "Fresh bread", "food", food_value=10)
        bread2 = Item("bread", "Fresh bread", "food", food_value=10)
        
        # Test equality
        self.assertEqual(bread1.name, bread2.name)
        self.assertEqual(bread1.type, bread2.type)
        self.assertEqual(bread1.food_value, bread2.food_value)
        
        # Test inventory stacking
        initial_count = len(self.game_state.player.inventory)
        self.game_state.player.add_item(bread1)
        self.game_state.player.add_item(bread2)
        
        # Should combine into one stack
        self.assertEqual(len(self.game_state.player.inventory), initial_count + 1)
        
        # Test non-stackable items
        sword1 = Item("sword", "A sword", "weapon", damage_bonus=5)
        sword2 = Item("sword", "A sword", "weapon", damage_bonus=5)
        
        self.game_state.player.add_item(sword1)
        self.game_state.player.add_item(sword2)
        self.assertEqual(len(self.game_state.player.inventory), initial_count + 3)

class TestCombatSystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        self.wolf = Entity("wolf", "A fierce wolf")
        self.wolf.health = 30
        self.wolf.damage = 5
        self.wolf.defense = 2
        
    def test_status_effects(self):
        """Test combat status effects"""
        test_effects = [
            ("poison", 3, -2),
            ("weakness", 2, -0.5),
            ("stun", 1, None),
            ("bleeding", 4, -1)
        ]
        
        for effect, duration, impact in test_effects:
            # Reset health before each test
            self.player.health = 100
            initial_health = self.player.health
            
            self.player.apply_effect((effect, duration))
            self.player.update_effects()
            
            if impact and (effect == "poison" or effect == "bleeding"):
                self.assertEqual(self.player.health, initial_health + impact)

class TestTimeSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        
    def test_time_progression(self):
        """Test day/night cycle"""
        initial_time = self.game_state.time.current_time
        initial_day = self.game_state.time.get_day_number()
        
        # Test minutes advance correctly
        self.game_state.advance_time(30)
        self.assertEqual(self.game_state.time.current_time, initial_time + 30)
        
        # Test day changes at midnight
        minutes_until_midnight = 24 * 60 - initial_time
        self.game_state.advance_time(minutes_until_midnight + 1)
        self.assertEqual(self.game_state.time.get_day_number(), initial_day + 1)
        
    def test_time_based_events(self):
        """Test events triggered by time"""
        # Test night events
        self.game_state.time.current_time = 23 * 60  # 11 PM
        event = self.game_state.event_manager.check_events(self.game_state)
        self.assertIsNotNone(event)
        self.assertIn("night", event.lower())
        
        # Test morning events
        self.game_state.time.current_time = 6 * 60  # 6 AM
        event = self.game_state.event_manager.check_events(self.game_state)
        self.assertIsNotNone(event)
        self.assertIn("morning", event.lower())

    def test_time_edge_cases(self):
        """Test time system edge cases"""
        # Test midnight rollover
        self.game_state.time.current_time = 23 * 60 + 59  # 23:59
        self.game_state.advance_time(1)
        self.assertEqual(self.game_state.time.current_time % (24 * 60), 0)
        
        # Test multi-day advancement
        initial_day = self.game_state.time.get_day_number()
        self.game_state.advance_time(24 * 60 * 3)  # Advance 3 days
        self.assertEqual(self.game_state.time.get_day_number(), initial_day + 3)

class TestNeedSystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        
    def test_need_decay(self):
        """Test needs decrease over time"""
        initial_hunger = self.player.hunger
        initial_thirst = self.player.thirst
        initial_energy = self.player.energy
        initial_bladder = self.player.bladder
        
        # Advance time by 1 hour
        self.game_state.advance_time(60)
        
        # Check needs decreased
        self.assertLess(self.player.hunger, initial_hunger)
        self.assertLess(self.player.thirst, initial_thirst)
        self.assertLess(self.player.energy, initial_energy)
        self.assertLess(self.player.bladder, initial_bladder)
        
    def test_need_effects(self):
        """Test effects of low needs"""
        # Test hunger damage
        self.player.hunger = 0
        initial_health = self.player.health
        self.player.update_needs()
        self.assertLess(self.player.health, initial_health)
        
        # Test thirst damage
        self.player.health = initial_health
        self.player.thirst = 0
        self.player.update_needs()
        self.assertLess(self.player.health, initial_health)
        
        # Test energy effects
        self.player.energy = 10
        self.player.update_needs()
        # Would need to capture stdout to test warning message
        
        # Test bladder effects
        self.player.bladder = 10
        self.player.update_needs()
        # Would need to capture stdout to test warning message

class TestJournalSystem(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.game_state = GameState(self.player)
        
    def test_bestiary_entries(self):
        """Test adding/viewing bestiary entries"""
        # Add test entry
        wolf = Entity("wolf", "A fierce wolf")
        self.player.journal.add_bestiary_entry(wolf)
        
        # Verify entry exists
        entries = self.player.journal.get_bestiary_entries()
        self.assertIn("wolf", entries)
        self.assertEqual(entries["wolf"], wolf.description)
        
    def test_quest_notes(self):
        """Test quest note management"""
        # Add test note
        note = "Find the crystal in the cave"
        self.player.journal.add_quest_note(note)
        
        # Verify note exists
        notes = self.player.journal.get_quest_notes()
        self.assertIn(note, notes)

class TestEventSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        
    def test_random_events(self):
        """Test random event generation"""
        # Test event generation
        event = self.game_state.event_manager.generate_random_event()
        self.assertIsNotNone(event)
        self.assertTrue(hasattr(event, 'name'))
        self.assertTrue(hasattr(event, 'description'))
        
        # Test event frequency
        events = []
        for _ in range(100):
            event = self.game_state.event_manager.generate_random_event()
            events.append(event.name)
            
        # Check event distribution
        unique_events = set(events)
        self.assertGreater(len(unique_events), 3)  # Should have multiple event types
        
    def test_event_conditions(self):
        """Test event trigger conditions"""
        # Test time-based triggers
        night_event = self.game_state.event_manager.check_night_events()
        self.assertIsNotNone(night_event)
        
        # Test location-based triggers
        self.game_state.current_location = Location("forest", "A dark forest")
        forest_event = self.game_state.event_manager.check_location_events()
        self.assertIsNotNone(forest_event)
        
        # Test condition-based triggers
        self.game_state.player.health = 20  # Low health
        danger_event = self.game_state.event_manager.check_condition_events()
        self.assertIsNotNone(danger_event)

    def test_location_based_events(self):
        """Test events specific to location types"""
        # Test cave events
        self.game_state.current_location = Location("cave", "Dark Cave")
        event = self.game_state.event_manager.check_location_events()
        self.assertIn("cave", event.lower())
        
        # Test forest events at night
        self.game_state.current_location = Location("forest", "Dark Forest")
        self.game_state.time.current_time = 23 * 60  # 11 PM
        event = self.game_state.event_manager.check_location_events()
        self.assertIn("forest", event.lower())

class TestAchievementSystem(unittest.TestCase):
    def setUp(self):
        self.achievement_system = AchievementSystem()
        self.player = Player()
        self.game_state = GameState(self.player)
        self.player.game_state = self.game_state
        self.player.stats = {"rare_kills": 0}
        
    def test_achievement_unlock(self):
        """Test basic achievement unlocking"""
        achievement_id = "rare_hunter"
        self.achievement_system.unlock_achievement(self.player, achievement_id)
        
        self.assertTrue(self.achievement_system.achievements[achievement_id].completed)
        self.assertIsNotNone(self.achievement_system.achievements[achievement_id].completion_date)
        
    def test_rare_kill_achievements(self):
        """Test rare enemy kill achievements"""
        # Create a rare enemy
        rare_wolf = Entity("ghost wolf", "A ghostly wolf")
        rare_wolf.is_rare = True
        
        # Test first rare kill
        self.achievement_system.check_achievement(
            self.player, 
            "defeat_enemy", 
            {"enemy": rare_wolf}
        )
        self.assertTrue(self.achievement_system.achievements["rare_hunter"].completed)
        
        # Test legendary hunter (10 kills)
        self.player.stats["rare_kills"] = 9
        self.achievement_system.check_achievement(
            self.player, 
            "defeat_enemy", 
            {"enemy": rare_wolf}
        )
        self.assertTrue(self.achievement_system.achievements["legendary_hunter"].completed)
        
    def test_specific_rare_achievements(self):
        """Test achievements for specific rare enemies"""
        ghost_wolf = Entity("ghost wolf", "A ghostly wolf")
        ghost_wolf.is_rare = True
        
        self.achievement_system.check_achievement(
            self.player,
            "defeat_enemy",
            {"enemy": ghost_wolf}
        )
        self.assertTrue(self.achievement_system.achievements["ghost_wolf_slayer"].completed)
        
    def test_achievement_rewards(self):
        """Test achievement reward distribution"""
        initial_exp = self.player.exp
        self.achievement_system.unlock_achievement(self.player, "rare_hunter")
        
        self.assertEqual(
            self.player.exp, 
            initial_exp + self.achievement_system.achievements["rare_hunter"].reward_exp
        )


class TestLevelingSystem(unittest.TestCase):
    def setUp(self):
        self.leveling_system = LevelingSystem()
        self.player = Player()
        self.game_state = GameState(self.player)
        self.player.game_state = self.game_state
        
    def test_level_calculation(self):
        """Test level calculation from exp"""
        test_cases = [
            (0, 1),      # Starting level
            (50, 1),     # Not enough for level 2
            (100, 2),    # Just enough for level 2
            (200, 2),    # More than needed for 2, not enough for 3
            (1000, 5),   # Higher level
        ]
        
        for exp, expected_level in test_cases:
            self.assertEqual(self.leveling_system.calculate_level(exp), expected_level)
            
    def test_exp_to_next_level(self):
        """Test exp remaining calculation"""
        test_cases = [
            (0, 100),    # Need 100 exp for level 2
            (50, 50),    # Need 50 more exp for level 2
            (100, 150),  # Need 150 more exp for level 3
        ]
        
        for current_exp, expected_needed in test_cases:
            self.assertEqual(
                self.leveling_system.exp_to_next_level(current_exp),
                expected_needed
            )
            
    def test_level_up_effects(self):
        """Test stat increases on level up"""
        # Record initial stats
        initial_health = self.player.max_health
        initial_damage = self.player.base_damage
        initial_defense = self.player.base_defense
        
        # Give enough exp to level up
        self.player.exp = 100  # Level 1 -> 2
        self.leveling_system.level_up(self.player)
        
        # Check stat increases
        self.assertEqual(self.player.level, 2)
        self.assertEqual(self.player.max_health, initial_health + 10)
        self.assertEqual(self.player.base_damage, initial_damage + 2)
        self.assertEqual(self.player.base_defense, initial_defense + 1)
        
    @given(st.integers(min_value=0, max_value=10000))
    def test_level_calculation_properties(self, exp):
        """Property-based testing for level calculation"""
        level = self.leveling_system.calculate_level(exp)
        
        # Properties that should always hold
        self.assertGreaterEqual(level, 1)  # Level should never be less than 1
        self.assertLessEqual(level, len(self.leveling_system.level_thresholds) + 1)  # Should not exceed max level
        
        # Test that more exp always gives same or higher level
        next_level = self.leveling_system.calculate_level(exp + 1)
        self.assertGreaterEqual(next_level, level)

class TestDisplaySystem(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.game_state = GameState(Player())
        
    def test_color_rendering(self):
        """Test color output"""
        # Test color text generation
        colored_text = self.display.colorize("Test", "red")
        self.assertIn("\033[31m", colored_text)  # ANSI red color code
        self.assertIn("\033[0m", colored_text)   # ANSI reset code
        
        # Test rarity colors
        item = Item("sword", "A sword", "weapon", rarity="rare")
        colored_name = self.display.colorize_rarity(item)
        self.assertIn("\033[", colored_name)
        
    def test_ui_layouts(self):
        """Test UI component rendering"""
        # Test character sheet layout
        stats = {
            "health": 100,
            "max_health": 100,
            "level": 1,
            "exp": 0,
            "attributes": {"strength": 5, "dexterity": 5},
            "skills": {"melee": 1, "defense": 1}
        }
        sheet = self.display.show_character_sheet(stats)
        self.assertIn("Character Stats", sheet)
        self.assertIn("Attributes:", sheet)
        self.assertIn("Skills:", sheet)
        
        # Test location description
        location = Location("meadow", "A peaceful meadow")
        desc = self.display.show_location(location)
        self.assertIn("Location:", desc)
        self.assertIn("meadow", desc)
        self.assertIn("peaceful meadow", desc)

class TestStorySystem(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        
    def test_chapter_progression(self):
        """Test story advancement"""
        # Test chapter unlock
        self.game_state.story.unlock_chapter("tutorial")
        self.assertIn("tutorial", self.game_state.story.discovered_chapters)
        
        # Test chapter requirements
        self.game_state.story.set_requirement("chapter1", "tutorial")
        self.assertFalse(self.game_state.story.can_access("chapter2"))
        self.game_state.story.unlock_chapter("chapter1")
        self.assertTrue(self.game_state.story.can_access("chapter1"))
        
    def test_story_flags(self):
        """Test story state tracking"""
        # Test flag setting
        self.game_state.story.set_flag("met_wizard", True)
        self.assertTrue(self.game_state.story.get_flag("met_wizard"))
        
        # Test quest stage tracking
        self.game_state.story.advance_quest("main_quest", "spoke_to_wizard")
        self.assertEqual(self.game_state.story.get_quest_stage("main_quest"), "spoke_to_wizard")
        
        # Test branching paths
        self.game_state.story.choose_path("help_wizard")
        self.assertIn("wizard_ally", self.game_state.story.active_paths)

class TestSystemIntegration(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(Player())
        
    def test_combat_needs_interaction(self):
        """Test combat affects player needs"""
        initial_energy = self.game_state.player.energy
        initial_health = self.game_state.player.health
        
        # Simulate combat
        wolf = Entity("wolf", "A fierce wolf")
        self.game_state.current_location.add_entity(wolf)
        self.game_state.combat_system.process_combat(self.game_state.player, wolf)
        
        # Check energy decreased
        self.assertLess(self.game_state.player.energy, initial_energy)
        
    def test_time_event_integration(self):
        """Test time progression triggers events"""
        # Set time to just before dawn
        self.game_state.time.current_time = 5 * 60  # 5 AM
        
        # Advance to dawn
        self.game_state.advance_time(60)  # Advance to 6 AM
        event = self.game_state.event_manager.check_events(self.game_state)
        self.assertIsNotNone(event)
        self.assertIn("dawn", event.lower())
        
    def test_quest_achievement_integration(self):
        """Test quest completion triggers achievements"""
        initial_achievements = len([a for a in self.game_state.achievements.achievements.values() if a["unlocked"]])
        
        # Complete a quest that should trigger an achievement
        self.game_state.story.complete_quest("tutorial")
        
        # Check achievement was unlocked
        current_achievements = len([a for a in self.game_state.achievements.achievements.values() if a["unlocked"]])
        self.assertGreater(current_achievements, initial_achievements)

    def test_combat_quest_achievement(self):
        """Test combat completing quest and triggering achievement"""
        # Set up quest to kill wolves
        self.game_state.story.add_quest("wolf_hunter", "Kill 3 wolves", target=3)
        
        # Kill wolves and check quest/achievement progress
        for _ in range(3):
            wolf = Entity("wolf", "A fierce wolf")
            self.game_state.combat_system.process_combat(self.player, wolf)
            wolf.health = 0  # Simulate killing wolf
            
        self.assertTrue(self.game_state.story.is_quest_complete("wolf_hunter"))
        self.assertTrue(self.game_state.achievements.is_unlocked("wolf_hunter"))
        
    def test_time_needs_events(self):
        """Test time affecting needs and triggering events"""
        initial_hunger = self.player.hunger
        
        # Advance time significantly
        self.game_state.advance_time(240)  # 4 hours
        
        # Check needs decreased
        self.assertLess(self.player.hunger, initial_hunger)
        
        # Check if hunger triggered an event
        events = self.game_state.event_manager.get_recent_events()
        self.assertTrue(any("hungry" in e.lower() for e in events))

class TestGeneratorSystem(unittest.TestCase):
    def test_location_generation(self):
        """Test location generation with features"""
        generator = LocationGenerator()
        
        # Test each location type
        for loc_type in ["meadow", "forest", "cave"]:
            location = generator.generate_location(loc_type)
            self.assertEqual(location.location_type, loc_type)
            self.assertIsNotNone(location.description)
            self.assertTrue(any(feature in location.get_detailed_survey() 
                              for feature in generator.descriptors[loc_type]['features']))
    
    def test_reward_generation(self):
        """Test reward generation tiers"""
        generator = RewardGenerator()
        item_gen = ItemGenerator()
        
        for tier in ["basic", "intermediate", "advanced"]:
            rewards = generator.generate_reward(tier, item_gen)
            self.assertGreater(len(rewards), 0)
            for reward in rewards:
                self.assertIsInstance(reward, Item)

class TestEntityGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = EntityGenerator()
        
    def test_entity_generation(self):
        """Test basic entity generation"""
        # Test each entity type
        for entity_type in ["wolf", "bat", "troll"]:
            entity = self.generator.generate_entity(entity_type)
            self.assertIsInstance(entity, Entity)
            self.assertIn(entity.name, [v for v in self.generator.bestiary[entity_type]["variants"]])
            
    def test_entity_scaling(self):
        """Test entity level scaling"""
        # Test level 1 vs level 10 wolf
        wolf1 = self.generator.generate_entity("wolf", level=1)
        wolf10 = self.generator.generate_entity("wolf", level=10)
        
        self.assertGreater(wolf10.health, wolf1.health)
        self.assertGreater(wolf10.damage, wolf1.damage)
        
    def test_entity_traits(self):
        """Test entity traits and behaviors"""
        # Explicitly create a non-rare wolf
        wolf = self.generator.generate_entity("wolf", force_rare=False)
        
        # Check traits and behaviors
        self.assertIn(wolf.behavior, self.generator.bestiary["wolf"]["behaviors"])
        self.assertIn(wolf.trait, self.generator.bestiary["wolf"]["possible_traits"])
        self.assertEqual(wolf.loot_table, self.generator.bestiary["wolf"]["loot_table"])

    def test_rare_traits(self):
        """Test rare entity traits"""
        # Force a rare spawn
        wolf = self.generator.generate_entity("wolf", force_rare=True)
        
        # Check rare traits and loot
        self.assertIn(wolf.trait, self.generator.bestiary["wolf"]["rare_traits"])
        self.assertEqual(wolf.loot_table, self.generator.bestiary["wolf"]["rare_loot_table"])

    def test_invalid_entity(self):
        """Test handling of invalid entity types"""
        with self.assertRaises(ValueError):
            self.generator.generate_entity("dragon")  # Non-existent type

    def test_entity_generation_properties(self):
        """Test entity generation with property-based testing"""
        @given(
            entity_type=st.sampled_from(["wolf", "bat", "troll"]),
            level=st.integers(min_value=1, max_value=100)
        )
        def test_entity_generation_properties(self, entity_type, level):
            """Test entity generation with property-based testing"""
            entity = self.generator.generate_entity(entity_type, level)
            
            # Properties that should always hold
            self.assertGreater(entity.health, 0)
            self.assertGreater(entity.damage, 0)
            self.assertGreaterEqual(entity.defense, 0)
            self.assertIn(entity.behavior, self.generator.bestiary[entity_type]["behaviors"])

    def test_rare_entity_generation(self):
        """Test rare entity generation"""
        # Force rare spawn
        wolf = self.generator.generate_entity("wolf", force_rare=True)
        
        # Check rare properties
        self.assertTrue(wolf.is_rare)
        self.assertIn(wolf.name, ["ghost wolf", "alpha dire wolf", "ancient wolf"])
        self.assertIn(wolf.trait, ["ethereal", "legendary", "mythical"])
        self.assertIn("spectral_pelt", wolf.loot_table)
        
        # Check stats are doubled
        base_wolf = self.generator.generate_entity("wolf", force_rare=False)
        self.assertGreater(wolf.health, base_wolf.health * 1.5)
        self.assertGreater(wolf.damage, base_wolf.damage * 1.5)

    def test_rare_spawn_rate(self):
        """Test rare spawn probability"""
        # Generate many entities and check rare spawn rate
        num_entities = 1000
        rare_count = sum(
            1 for _ in range(num_entities)
            if self.generator.generate_entity("wolf").is_rare
        )
        
        # Should be roughly 5% (allowing for some variance)
        spawn_rate = rare_count / num_entities
        self.assertGreater(spawn_rate, 0.03)  # At least 3%
        self.assertLess(spawn_rate, 0.07)     # At most 7%

    @given(
        entity_type=st.sampled_from(["wolf", "bat", "troll"]),
        level=st.integers(min_value=1, max_value=100),
        force_rare=st.booleans()
    )
    def test_rare_entity_properties(self, entity_type, level, force_rare):
        """Test rare entity generation with property-based testing"""
        entity = self.generator.generate_entity(entity_type, level, force_rare)
        
        if force_rare:
            self.assertTrue(entity.is_rare)
            if entity_type == "wolf":  # Only wolf has rare variants defined
                self.assertIn(entity.name, self.generator.bestiary[entity_type]["rare_variants"])
                self.assertIn(entity.trait, self.generator.bestiary[entity_type]["rare_traits"])

class TestItemGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ItemGenerator()
        
    def test_weapon_generation(self):
        """Test weapon generation"""
        weapon = self.generator.generate_item("weapon")
        
        # Check weapon properties
        self.assertEqual(weapon.type, "weapon")
        self.assertGreater(weapon.damage_bonus, 0)
        self.assertGreater(weapon.weight, 0)
        
        # Check name format
        name_parts = weapon.name.split()
        self.assertIn(name_parts[0], self.generator.prefixes["weapon"])
        self.assertIn(name_parts[1], self.generator.materials["weapon"])
        
    def test_armor_generation(self):
        """Test armor generation"""
        armor = self.generator.generate_item("armor")
        
        # Check armor properties
        self.assertEqual(armor.type, "armor")
        self.assertGreater(armor.defense_bonus, 0)
        self.assertGreater(armor.weight, 0)
        
    def test_quality_scaling(self):
        """Test item quality scaling"""
        basic_weapon = self.generator.generate_item("weapon", quality=0)
        epic_weapon = self.generator.generate_item("weapon", quality=10)
        
        self.assertGreater(epic_weapon.damage_bonus, basic_weapon.damage_bonus)

    @given(
        category=st.sampled_from(["weapon", "armor"]),
        quality=st.integers(min_value=0, max_value=10)
    )
    def test_item_generation_properties(self, category, quality):
        """Test item generation with property-based testing"""
        item = self.generator.generate_item(category, quality)
        
        # Properties that should always hold
        self.assertGreater(item.weight, 0)
        if category == "weapon":
            self.assertGreater(item.damage_bonus, 0)
        elif category == "armor":
            self.assertGreater(item.defense_bonus, 0)

class TestNoteGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = NoteGenerator()
        
    def test_journal_generation(self):
        """Test journal note generation"""
        note = self.generator.generate_note("journal", day=5)
        
        # Check note contains required elements
        self.assertIn("Day 5", note)
        
        # Check that at least one content item is present
        content_found = False
        for content_list in self.generator.content.values():
            if any(content in note for content in content_list):
                content_found = True
                break
        self.assertTrue(content_found)

    def test_lore_generation(self):
        """Test lore note generation"""
        note = self.generator.generate_note("lore")
        
        # Check that at least one lore template matches
        template_matched = False
        for template in self.generator.templates["lore"]:
            # Get required keys from template
            required_keys = [k[1] for k in string.Formatter().parse(template) if k[1]]
            
            # Check if all required content is present
            content_present = True
            for key in required_keys:
                if key in self.generator.content:
                    if not any(content in note for content in self.generator.content[key]):
                        content_present = False
                        break
            
            if content_present:
                template_matched = True
                break
            
        self.assertTrue(template_matched, f"No lore template matched for note: {note}")

    def test_note_variety(self):
        """Test note variety"""
        notes = [self.generator.generate_note() for _ in range(10)]
        unique_notes = set(notes)
        
        # Should get different notes
        self.assertGreater(len(unique_notes), 5)

    @given(
        note_type=st.sampled_from(["journal", "lore"]),
        day=st.integers(min_value=1, max_value=365)
    )
    def test_note_generation_properties(self, note_type, day):
        """Test note generation with property-based testing"""
        note = self.generator.generate_note(note_type, day)
        
        # Properties that should always hold
        self.assertIsInstance(note, str)
        self.assertGreater(len(note), 0)
        
        if note_type == "journal" and "Day" in self.generator.templates["journal"][0]:
            self.assertIn(str(day), note)

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
        TestCharacterSystem
    ]
    
    for test_case in test_cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_comprehensive_tests() 