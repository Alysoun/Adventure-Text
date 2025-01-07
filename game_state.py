import random
from base_classes import Location
from items import Item
from entities import Entity
from save_system import SaveSystem
from story import StoryManager
from time_manager import TimeManager
from events import EventManager
from generators import LocationGenerator, ItemGenerator, EntityGenerator, RewardGenerator
from achievements import AchievementManager
from world_generator import WorldGenerator
from combat_system import CombatSystem
from command_parser import CommandParser
from display import Display

class GameState:
    def __init__(self, player):
        # Initialize basic attributes first
        self.player = player
        self.current_location = None
        self.discovered_locations = {}
        self.quest_log = []
        self.discovered_areas = set()
        self.milestones = {
            "wolves_befriended": False,
            "cave_discovered": False,
            "crystal_found": False
        }
        
        # Initialize systems
        self.save_system = SaveSystem()
        self.time = TimeManager()
        self.event_manager = EventManager()
        self.achievements = AchievementManager()
        self.story = StoryManager()
        self.combat_system = CombatSystem()
        self.combat_system.set_player(player)
        self.command_parser = CommandParser()
        
        # Initialize generators
        self.world_generator = WorldGenerator()
        self.location_generator = LocationGenerator()
        self.item_generator = ItemGenerator()
        self.entity_generator = EntityGenerator()
        self.reward_generator = RewardGenerator()
        
        # Set up starting location last
        starting_location = self.world_generator._generate_meadow()
        self.set_current_location(starting_location)
        
    def set_current_location(self, location):
        """Set the current location"""
        if location is None:
            return
            
        self.current_location = location
        if not hasattr(self.current_location, 'items'):
            self.current_location.items = []
        if not hasattr(self.current_location, 'entities'):
            self.current_location.entities = []
        if location.id not in self.discovered_locations:
            self.discovered_locations[location.id] = location
            
    def get_location(self, location_id):
        return self.discovered_locations.get(location_id)
        
    def generate_location(self):
        location_types = {
            'meadow': self._generate_meadow,
            'forest': self._generate_forest,
            'cave': self._generate_cave
        }
        location_type = random.choice(list(location_types.keys()))
        return location_types[location_type]()
        
    def _generate_meadow(self):
        description = "You are in a peaceful meadow. Tall grass sways in the gentle breeze."
        location = Location("meadow", description)
        
        # Add random features
        if random.random() < 0.3:
            location.add_entity(Entity("dead_body", "A lifeless body lies in the grass"))
        if random.random() < 0.2:
            location.add_item(Item("flower", "A beautiful wildflower"))
            
        return location
        
    def _generate_forest(self):
        description = "You are in a dense forest. Tall trees surround you, their branches swaying gently overhead."
        location = Location("forest", description)
        
        # Add random features
        if random.random() < 0.4:
            location.add_item(Item("mushroom", "A mysterious looking mushroom grows at the base of a tree"))
        if random.random() < 0.3:
            location.add_entity(Entity("wolf", "A grey wolf watches you cautiously"))
        
        return location
        
    def _generate_cave(self):
        description = "You are in a dark cave. The air is cool and damp."
        location = Location("cave", description)
        
        # Add random features
        if random.random() < 0.4:
            location.add_item(Item("crystal", "A glowing crystal protrudes from the wall"))
        if random.random() < 0.2:
            location.add_entity(Entity("bat", "A bat hangs from the ceiling"))
            
        return location 
        
    def advance_time(self, minutes):
        new_day = self.time.advance_time(minutes)
        if new_day:
            self.save_system.save_game(self, "autosave.json")
            print("\nA new day begins... Game auto-saved.")
        self.player.update_needs()
        
        # Check for time-based events
        event = self.event_manager.check_events(self)
        if event:
            print(f"\n{event}") 