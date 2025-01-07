import random
from base_classes import Location
from items import Item
from entities import Entity

class WorldGenerator:
    def __init__(self):
        self.starting_meadow_generated = False
        self.location_types = {
            'meadow': self._generate_meadow,
            'forest': self._generate_forest,
            'cave': self._generate_cave
        }
        
    def generate_location(self, location_type):
        """Generate a location of the specified type"""
        if location_type == "meadow":
            return self._generate_meadow()
        if location_type in self.location_types:
            return self.location_types[location_type]()
        return self._generate_random_location()
        
    def _generate_meadow(self):
        """Generate the starting meadow location"""
        location = Location("meadow", "A peaceful meadow")
        location.description = "You find yourself in a peaceful meadow surrounded by tall grass..."
        
        # Add starting note as a quest item
        if not self.starting_meadow_generated:
            note = Item(
                name="mysterious note",
                description="An old parchment with elegant script",
                item_type="quest_item",
                rarity=Item.QUEST  # Make it cyan to indicate quest item
            )
            location.add_item(note)
            self.starting_meadow_generated = True
        
        return location
        
    def _generate_forest(self, game_state):
        description = game_state.location_generator.generate_description("forest")
        location = Location("forest", description)
        
        # Add random features
        if random.random() < 0.4:
            location.add_item(game_state.item_generator.generate_item())
        if random.random() < 0.3:
            location.add_entity(game_state.entity_generator.generate_entity("wolf", "hostile"))
        
        return location
        
    def _generate_cave(self, game_state):
        description = game_state.location_generator.generate_description("cave")
        location = Location("cave", description)
        
        # Add random features
        if random.random() < 0.4:
            location.add_item(game_state.item_generator.generate_item())
        if random.random() < 0.2:
            location.add_entity(game_state.entity_generator.generate_entity("bat", "neutral"))
            
        return location
        
    def _generate_random_location(self):
        location_type = random.choice(list(self.location_types.keys()))
        return self.location_types[location_type]() 