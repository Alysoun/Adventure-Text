import json
import os

class SaveSystem:
    def __init__(self):
        self.save_dir = "saves"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_game(self, game_state, filename):
        """Save game state to file"""
        save_data = {
            "player": {
                "inventory": [(item.name, item.type) for item in game_state.player.inventory],
                "health": game_state.player.health,
                "equipped": {
                    slot: item.name if item else None 
                    for slot, item in game_state.player.equipped.items()
                },
                "stats": {
                    "hunger": game_state.player.hunger,
                    "thirst": game_state.player.thirst,
                    "energy": game_state.player.energy
                }
            },
            "location": {
                "type": game_state.current_location.location_type,
                "items": [item.name for item in game_state.current_location.items],
                "entities": [entity.name for entity in game_state.current_location.entities]
            },
            "story": {
                "quest_stages": game_state.story.quest_stages,
                "discovered_chapters": list(game_state.story.discovered_chapters),  # Convert set to list
                "milestones": game_state.milestones
            },
            "world": {
                "discovered_areas": list(game_state.discovered_areas),  # Convert set to list
                "time": game_state.time.current_time
            }
        }
        
        with open(os.path.join(self.save_dir, filename), 'w') as f:
            json.dump(save_data, f)
            
    def load_game(self, game_state, filename):
        """Load game state from file"""
        with open(os.path.join(self.save_dir, filename), 'r') as f:
            save_data = json.load(f)
            
        # Restore player state
        game_state.player.health = save_data["player"]["health"]
        
        # Restore inventory with proper type info
        game_state.player.inventory = []
        for item_name, item_type in save_data["player"]["inventory"]:
            item = game_state.item_generator.generate_item(item_type)
            if item:
                game_state.player.inventory.append(item)
                
        # Restore equipped items
        for slot, item_name in save_data['player']['equipped'].items():
            if item_name:
                item = game_state.item_generator.generate_item_by_name(item_name)
                game_state.player.equipped[slot] = item
                
        # Restore player stats
        stats = save_data['player']['stats']
        game_state.player.hunger = stats['hunger']
        game_state.player.thirst = stats['thirst']
        game_state.player.energy = stats['energy']
        
        # Restore story state
        game_state.story.quest_stages = save_data['story']['quest_stages']
        game_state.story.discovered_chapters = set(save_data['story']['discovered_chapters'])
        game_state.milestones = save_data['story']['milestones']
        
        # Restore world state
        game_state.discovered_areas = set(save_data['world']['discovered_areas'])
        game_state.time.current_time = save_data['world']['time']
        
        return game_state  # Return the updated game state 