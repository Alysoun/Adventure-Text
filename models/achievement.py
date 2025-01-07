class Achievement:
    def __init__(self, name, description, reward_exp=0):
        self.name = name
        self.description = description
        self.completed = False
        self.reward_exp = reward_exp
        self.completion_date = None

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            # Combat achievements
            "rare_hunter": Achievement(
                "Rare Hunter", 
                "Defeat your first rare enemy",
                reward_exp=100
            ),
            "legendary_hunter": Achievement(
                "Legendary Hunter",
                "Defeat 10 rare enemies",
                reward_exp=500
            ),
            "ghost_wolf_slayer": Achievement(
                "Ghost Wolf Slayer",
                "Defeat the mythical Ghost Wolf",
                reward_exp=250
            ),
            
            # Collection achievements
            "rare_collector": Achievement(
                "Rare Collector",
                "Collect 5 different rare items",
                reward_exp=200
            ),
            
            # Discovery achievements
            "secret_finder": Achievement(
                "Secret Finder",
                "Discover a hidden location",
                reward_exp=150
            )
        }
        
    def check_achievement(self, player, trigger, context):
        """Check if an achievement should be unlocked"""
        if trigger == "defeat_enemy" and context.get("enemy").is_rare:
            rare_kills = player.stats.get("rare_kills", 0)
            
            if rare_kills == 0:
                self.unlock_achievement(player, "rare_hunter")
            if rare_kills == 9:
                self.unlock_achievement(player, "legendary_hunter")
            if context["enemy"].name == "ghost wolf":
                self.unlock_achievement(player, "ghost_wolf_slayer")
                
    def unlock_achievement(self, player, achievement_id):
        """Unlock an achievement and grant its rewards"""
        achievement = self.achievements[achievement_id]
        if not achievement.completed:
            achievement.completed = True
            achievement.completion_date = player.game_state.time.current_time
            
            # Grant rewards
            player.gain_exp(achievement.reward_exp)
            
            # Notify player
            player.game_state.display.show_message(
                f"Achievement Unlocked: {achievement.name}!\n"
                f"{achievement.description}\n"
                f"Reward: {achievement.reward_exp} XP"
            ) 