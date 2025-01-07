class Journal:
    def __init__(self):
        self.discovered_entities = {}
        self.discovered_locations = {}
        self.quest_notes = []
        
    def add_entity_entry(self, entity_type):
        if entity_type.name not in self.discovered_entities:
            self.discovered_entities[entity_type.name] = entity_type
            
    def add_location_entry(self, location):
        if location.location_type not in self.discovered_locations:
            self.discovered_locations[location.location_type] = location
            
    def add_quest_note(self, note):
        self.quest_notes.append(note)
        
    def show_bestiary(self):
        print("\n=== Bestiary ===")
        for name, entity in self.discovered_entities.items():
            print(f"\n{name.upper()}")
            print(f"Description: {entity.description}")
            print(f"Story: {entity.story}") 
        
    def show_quest_notes(self):
        print("\n=== Quest Notes ===")
        if not self.quest_notes:
            print("No quest information recorded yet.")
            return
            
        for i, note in enumerate(self.quest_notes, 1):
            print(f"\nEntry {i}:")
            print(note) 