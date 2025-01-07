import random
from generators import LocationGenerator, ItemGenerator, EntityGenerator


class Location:
    def __init__(self, location_type, name):
        self.id = id(self)  # Add unique ID
        self.location_type = location_type
        self.name = name
        self.description = ""
        self.items = []
        self.entities = []
        self.connections = {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        }
        
    def add_item(self, item):
        """Add an item to this location"""
        self.items.append(item)
        
    def add_entity(self, entity):
        """Add an entity to this location"""
        self.entities.append(entity)
        
    def remove_item(self, item):
        """Remove an item from this location"""
        self.items.remove(item)
        
    def get_description(self):
        """Get the full description including items and entities"""
        desc = self.description
        
        if self.items:
            desc += "\nYou see: " + ", ".join(str(item) for item in self.items)
            
        if self.entities:
            desc += "\nPresent here: " + ", ".join(str(entity) for entity in self.entities)
            
        return desc
        
    def search(self, target, game_state):
        """Search for items or entities"""
        for item in self.items:
            if target.lower() in item.name.lower():
                return item.search()
                
        for entity in self.entities:
            if target.lower() in entity.name.lower():
                return entity.search(game_state)
                
        return f"You find nothing special about the {target}"
        
    def move_direction(self, direction):
        """Return the connected location in the given direction"""
        return self.connections.get(direction) 