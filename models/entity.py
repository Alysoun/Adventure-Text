import random

class Entity:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.health = 0
        self.damage = 0
        self.defense = 0
        self.speed = 1.0
        self.dodge_chance = 0.1
        self.aggression = 1.0
        self.abilities = []
        
    def use_ability(self, ability_name, target=None, game_state=None):
        """Use a special ability"""
        if ability_name not in self.abilities:
            return False
            
        if ability_name == "call_pack":
            # Spawn 1-3 regular wolves
            num_wolves = random.randint(1, 3)
            for _ in range(num_wolves):
                wolf = game_state.entity_generator.generate_entity("wolf", force_rare=False)
                game_state.current_location.add_entity(wolf)
            return True
            
        elif ability_name == "life_drain":
            # Heal for 50% of damage dealt
            if target and hasattr(target, "health"):
                damage = self.calculate_damage()
                self.health = min(self.max_health, self.health + damage * 0.5)
                return True
                
        elif ability_name == "rage":
            # Increase damage as health decreases
            rage_bonus = (1 - (self.health / self.max_health)) * 2
            self.damage = self.base_damage * (1 + rage_bonus)
            return True
            
        return False 