class CombatSystem:
    def __init__(self):
        self.player = None
        
    def set_player(self, player):
        self.player = player
        
    def gain_combat_exp(self, amount):
        """Increase melee combat experience"""
        if self.player:
            self.player.skills['melee'] += amount // 10
        
    def gain_defense_exp(self, amount):
        """Increase defense experience"""
        if self.player:
            self.player.skills['defense'] += amount // 10 