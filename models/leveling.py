class LevelingSystem:
    def __init__(self):
        self.level_thresholds = [
            100,  # Level 1->2
            250,  # Level 2->3
            500,  # Level 3->4
            1000, # Level 4->5
            # ... etc
        ]
        
    def calculate_level(self, exp):
        """Calculate level based on total exp"""
        level = 1
        for threshold in self.level_thresholds:
            if exp >= threshold:
                level += 1
            else:
                break
        return level
        
    def exp_to_next_level(self, current_exp):
        """Calculate exp needed for next level"""
        current_level = self.calculate_level(current_exp)
        if current_level > len(self.level_thresholds):
            return None  # Max level reached
        return self.level_thresholds[current_level - 1] - current_exp
        
    def level_up(self, player):
        """Handle level up effects"""
        old_level = player.level
        new_level = self.calculate_level(player.exp)
        
        if new_level > old_level:
            player.level = new_level
            # Grant level up bonuses
            player.max_health += 10
            player.health = player.max_health  # Heal on level up
            player.base_damage += 2
            player.base_defense += 1
            
            # Notify player
            player.game_state.display.show_message(
                f"Level Up! You are now level {new_level}!\n"
                f"Health +10\n"
                f"Damage +2\n"
                f"Defense +1"
            ) 