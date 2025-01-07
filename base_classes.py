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
        
    def look_direction(self, direction):
        """Look in a specific direction"""
        if direction not in self.connections:
            return f"You can't look {direction}."
            
        if self.connections[direction]:
            connected = self.connections[direction]
            return f"To the {direction} you see {connected.name}."
        else:
            descriptions = {
                'meadow': {
                    'north': "Rolling hills stretch into the distance.",
                    'south': "The meadow continues, dotted with wildflowers.",
                    'east': "A dense forest looms ahead.",
                    'west': "The grass sways in the breeze."
                },
                'forest': {
                    'north': "The forest grows darker and thicker.",
                    'south': "Trees thin out towards a meadow.",
                    'east': "Ancient trees block most of the light.",
                    'west': "You see a path winding through the trees."
                },
                'cave': {
                    'north': "The cave walls glisten with moisture.",
                    'south': "The cave entrance lets in some light.",
                    'east': "The cave extends into darkness.",
                    'west': "Crystal formations catch what little light there is."
                }
            }
            
            if self.location_type in descriptions:
                return descriptions[self.location_type].get(direction, 
                    f"You see nothing special to the {direction}.")
            return f"You see nothing special to the {direction}."
            
    def get_detailed_survey(self, game_state=None):
        """Get detailed observations about the location"""
        details = []
        
        # Add environment details based on location type
        if self.location_type == "meadow":
            details.extend([
                "Butterflies flit between the wildflowers.",
                "A gentle breeze rustles through the tall grass.",
                "Small trails wind through the vegetation."
            ])
        elif self.location_type == "forest":
            details.extend([
                "Sunlight filters through the canopy above.",
                "The forest floor is covered in fallen leaves.",
                "Bird songs echo through the trees."
            ])
        elif self.location_type == "cave":
            details.extend([
                "Water drips somewhere in the darkness.",
                "The air is cool and damp.",
                "Crystals glint in the cave walls."
            ])
            
        # Add details about items
        if self.items:
            details.append(f"You notice {', '.join(str(item) for item in self.items)}.")
            
        # Add details about entities
        if self.entities:
            details.append(f"You see {', '.join(str(entity) for entity in self.entities)}.")
            
        return details 