import random
from items import Item

class Entity:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.inventory = []
        self.hostile = False
        self.health = 20  # Default health
        self.damage = 3   # Default damage
        self.defense = 0  # Default defense
        self.dodge_chance = 0.1  # Base 10% dodge chance
        self.crit_chance = 0.1   # Base 10% crit chance
        self.special_attacks = []
        
        # Entity-specific initialization
        if name == "wolf":
            self.hostile = True
            self.health = 30
            self.damage = 8
            self.defense = 2
            self.dodge_chance = 0.15
            self.crit_chance = 0.2
            self.special_attacks = [
                ("Fierce Bite", 1.5, 0.3),  # (name, damage_mult, chance)
                ("Pack Call", 1.2, 0.2)     # Might summon another wolf
            ]
        elif name == "bandit":
            self.hostile = True
            self.health = 40
            self.damage = 6
            self.defense = 3
            self.dodge_chance = 0.2
            self.special_attacks = [
                ("Backstab", 2.0, 0.15),
                ("Disarm", 0.5, 0.25)  # Reduces player damage temporarily
            ]
        elif name == "spider":
            self.hostile = True
            self.health = 25
            self.damage = 5
            self.defense = 1
            self.dodge_chance = 0.25
            self.special_attacks = [
                ("Web Shot", 0.8, 0.3),  # Reduces dodge chance
                ("Poison Bite", 1.2, 0.2)  # DOT effect
            ]
            
        # Add random items to certain entities when they're created
        if name == "dead body":
            if random.random() < 0.2:  # 20% chance of finding nothing
                self.inventory = []
            else:
                possible_items = [
                    Item("gold coins", "A handful of golden coins"),
                    Item("dagger", "A rusty but serviceable dagger"),
                    Item("letter", "A weathered letter with mysterious contents"),
                    Item("brass key", "An ornate brass key"),
                    Item("silver ring", "A silver ring with strange markings")
                ]
                # Add 1-3 random items to the body
                for _ in range(random.randint(1, 3)):
                    if random.random() < 0.7:  # 70% chance per item slot
                        self.inventory.append(random.choice(possible_items))
    
    def __str__(self):
        return self.name
        
    def search(self, game_state):
        if not self.inventory:
            if self.name == "dead body":
                return "You search the corpse thoroughly but find nothing of value."
            return f"You search the {self.name} but find nothing of interest."
            
        items_found = ", ".join(str(item) for item in self.inventory)
        result = f"You search the {self.name} and find: {items_found}"
        
        # Move items to the location
        for item in self.inventory:
            game_state.current_location.add_item(item)
        self.inventory.clear()
        
        return result 
        
    def attack(self, game_state):
        if self.name == "dead body":
            return "That seems rather pointless..."
        elif self.name == "bat":
            return "The bat quickly flies out of your reach, circling above."
        elif self.name == "wolf":
            return "The wolf growls menacingly and bares its teeth. It might be better to try feeding it..."
            
    def talk(self, game_state):
        if self.name == "dead body":
            return "The dead tell no tales..."
        elif self.name == "bat":
            return "The bat squeaks in response, but you can't understand it."
        elif self.name == "wolf":
            return "The wolf stares at you hungrily, perhaps it would be more interested in food."
            
    def feed(self, item, game_state):
        if self.name == "dead body":
            return "That would be a waste of food."
        elif self.name == "bat":
            if "fruit" in item.name.lower():
                game_state.player.remove_item(item)
                return "The bat eagerly takes the fruit and drops its silver chain!"
            return "The bat doesn't seem interested in that."
        elif self.name == "wolf":
            if "meat" in item.name.lower():
                self.hostile = False
                game_state.player.remove_item(item)
                return "The wolf devours the meat and seems much friendlier now!"
            return "The wolf only seems interested in meat." 
        
    def combat_round(self, player_damage, game_state):
        result = {'message': '', 'player_damage': 0, 'effects': []}
        
        if self.name == "dead body":
            result['message'] = "That seems rather pointless..."
            return result
            
        # Player's attack phase
        if random.random() < self.dodge_chance:
            result['message'] = f"The {self.name} dodges your attack!"
        else:
            # Calculate damage with critical hit chance
            is_crit = random.random() < game_state.player.crit_chance
            damage_mult = 2.0 if is_crit else 1.0
            damage_to_entity = max(0, int((player_damage - self.defense) * damage_mult))
            
            crit_text = " (Critical Hit!)" if is_crit else ""
            self.health -= damage_to_entity
            result['message'] = f"You hit the {self.name} for {damage_to_entity} damage{crit_text}! ({self.health} HP remaining)"
            
        # Entity's response phase
        if self.health <= 0:
            result['message'] = f"You defeated the {self.name}!"
            self._drop_loot(game_state)
            game_state.current_location.entities.remove(self)
        elif self.hostile:
            # Check for special attack
            special_attack = self._choose_special_attack()
            if special_attack:
                name, damage_mult, _ = special_attack
                damage_to_player = max(0, int(self.damage * damage_mult))
                result['player_damage'] = damage_to_player
                result['message'] += f"\nThe {self.name} uses {name}!"
                
                # Add special effects
                if name == "Poison Bite":
                    result['effects'].append(('poison', 3))  # 3 turns of poison
                elif name == "Web Shot":
                    result['effects'].append(('reduced_dodge', 2))
                elif name == "Disarm":
                    result['effects'].append(('reduced_damage', 2))
                elif name == "Pack Call" and random.random() < 0.5:
                    self._summon_ally(game_state)
                    result['message'] += f"\nThe {self.name}'s howl attracts another wolf!"
            else:
                # Normal attack with dodge chance
                if random.random() < game_state.player.dodge_chance:
                    result['message'] += f"\nYou dodge the {self.name}'s attack!"
                else:
                    is_crit = random.random() < self.crit_chance
                    damage_mult = 2.0 if is_crit else 1.0
                    damage_to_player = max(0, int(self.damage * damage_mult))
                    result['player_damage'] = damage_to_player
                    crit_text = " (Critical Hit!)" if is_crit else ""
                    result['message'] += f"\nThe {self.name} attacks you back for {damage_to_player} damage{crit_text}!"
                
        return result
        
    def _drop_loot(self, game_state):
        # Drop any inventory items
        for item in self.inventory:
            game_state.current_location.add_item(item)
            
        # Generate random loot based on entity type
        if self.name == "wolf":
            if random.random() < 0.5:
                game_state.current_location.add_item(
                    game_state.item_generator.generate_item("weapon", quality_level=2)
                )
        elif self.name == "bandit":
            if random.random() < 0.7:
                game_state.current_location.add_item(
                    game_state.item_generator.generate_item(random.choice(["weapon", "armor"]))
                ) 
        
    def _choose_special_attack(self):
        for attack in self.special_attacks:
            name, damage_mult, chance = attack
            if random.random() < chance:
                return attack
        return None
        
    def _summon_ally(self, game_state):
        if self.name == "wolf":
            new_wolf = game_state.entity_generator.generate_entity("wolf", "hostile")
            new_wolf.health = int(new_wolf.health * 0.7)  # Summoned allies are weaker
            game_state.current_location.add_entity(new_wolf) 