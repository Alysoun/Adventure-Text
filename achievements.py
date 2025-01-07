class AchievementManager:
    def __init__(self):
        self.achievements = {
            "first_steps": {
                "name": "First Steps",
                "description": "Move to a new location",
                "unlocked": False,
                "difficulty": "basic",
                "reward": None
            },
            "survivalist": {
                "name": "Survivalist",
                "description": "Cook your first meal",
                "unlocked": False,
                "difficulty": "basic",
                "reward": None
            },
            "wolf_whisperer": {
                "name": "Wolf Whisperer",
                "description": "Befriend a wolf without taking damage",
                "unlocked": False,
                "difficulty": "intermediate",
                "reward": None
            },
            "treasure_hunter": {
                "name": "Treasure Hunter",
                "description": "Find 5 valuable items",
                "unlocked": False,
                "progress": 0,
                "target": 5,
                "difficulty": "intermediate",
                "reward": None
            },
            "master_chef": {
                "name": "Master Chef",
                "description": "Create 3 different types of meals",
                "unlocked": False,
                "progress": set(),
                "target": 3,
                "difficulty": "intermediate",
                "reward": None
            },
            "explorer": {
                "name": "Explorer",
                "description": "Discover all location types",
                "unlocked": False,
                "progress": set(),
                "target": 3,
                "difficulty": "advanced",
                "reward": None
            }
        }

    def unlock(self, achievement_id):
        """Alias for unlock_achievement for simpler API"""
        return self.unlock_achievement(achievement_id, None)  # Pass None for game_state since we don't need rewards here
        
    def unlock_achievement(self, name, game_state):
        """Unlock an achievement and generate rewards if game_state provided"""
        ach = self.achievements[name]
        if not ach["unlocked"]:
            ach["unlocked"] = True
            
            if game_state:  # Only generate rewards if game_state provided
                # Generate rewards
                rewards = game_state.reward_generator.generate_reward(
                    ach["difficulty"], 
                    game_state.item_generator
                )
                
                # Give rewards to player
                for item in rewards:
                    game_state.player.add_item(item)
                    
                # Format reward message
                reward_msg = "\n".join(f"- {item.name}" for item in rewards)
                return f"\n🏆 Achievement Unlocked: {name} - {ach['description']}\n\nRewards:\n{reward_msg}"
                
        return None

    def check_achievement(self, game_state, action, context):
        updates = []
        
        if action == "move":
            if not self.achievements["first_steps"]["unlocked"]:
                updates.append(self.unlock_achievement("first_steps", game_state))
                
        elif action == "cook":
            if not self.achievements["survivalist"]["unlocked"]:
                updates.append(self.unlock_achievement("survivalist", game_state))
            
            # Check master chef
            meal_type = context.get("meal_type")
            if meal_type:
                ach = self.achievements["master_chef"]
                if not ach["unlocked"]:
                    ach["progress"].add(meal_type)
                    if len(ach["progress"]) >= ach["target"]:
                        ach["unlocked"] = True
                        updates.append(self._format_achievement("Master Chef"))
                        
        elif action == "discover_location":
            location_type = context.get("location_type")
            if location_type:
                ach = self.achievements["explorer"]
                if not ach["unlocked"]:
                    ach["progress"].add(location_type)
                    if len(ach["progress"]) >= ach["target"]:
                        ach["unlocked"] = True
                        updates.append(self._format_achievement("Explorer"))
                        
        return [update for update in updates if update]
        
    def _format_achievement(self, name):
        return f"\n🏆 Achievement Unlocked: {name} - {self.achievements[name]['description']}" 

    def is_unlocked(self, achievement_id):
        """Check if an achievement is unlocked"""
        return self.achievements.get(achievement_id, {"unlocked": False})["unlocked"]
        
    def get_progress(self, achievement_id):
        """Get progress for an achievement"""
        return self.achievements.get(achievement_id, {}).get("progress", 0)
        
    def get_all_progress(self):
        """Get progress for all achievements"""
        return {id: ach.get("progress", 0) 
                for id, ach in self.achievements.items() 
                if "progress" in ach} 