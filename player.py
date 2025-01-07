from journal import Journal
from items import Item

class Player:
    def __init__(self):
        self.inventory = []  # Start with empty inventory, not the note
        self.health = 100
        self._base_max_health = 100
        self.equipped = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        self.damage = 5  # Base damage
        self.defense = 0  # Base defense
        self.journal = Journal()
        self.hunger = 100
        self.thirst = 100
        self.energy = 100
        self.bladder = 100
        self._base_dodge_chance = 0.15
        self.crit_chance = 0.15
        self.status_effects = {}  # {effect_name: turns_remaining}
        
        # Add starting items
        self.add_item(Item(
            "mysterious note", 
            "A weathered note with cryptic writing. It seems important...",
            "quest_item"
        ))
        
        # Add RPG stats
        self.level = 1
        self.exp = 0
        self.gold = 100
        
        # Base attributes
        self.strength = 5      # Melee damage
        self.dexterity = 5     # Dodge chance
        self.intelligence = 5   # Magic power
        self.vitality = 5      # Health bonus
        self.charisma = 5      # NPC interactions
        self.wisdom = 5        # Experience gain
        self.luck = 5          # Critical hits & loot
        
        # Skills
        self.skills = {
            'melee': 1,
            'defense': 1,
            'survival': 1,
            'crafting': 1
        }
        
    def equip(self, item):
        """Equip an item"""
        if item not in self.inventory:
            self.inventory.append(item)  # Add item if not in inventory
        
        if item.type == "weapon":
            if self.equipped['weapon']:
                self.inventory.append(self.equipped['weapon'])
            self.equipped['weapon'] = item
        elif item.type == "armor":
            if self.equipped['armor']:
                self.inventory.append(self.equipped['armor'])
            self.equipped['armor'] = item
        
        self.inventory.remove(item)
            
    def get_stats(self):
        """Calculate total damage and defense including stat bonuses"""
        total_damage = self.damage + (self.strength - 5)  # Base damage + strength bonus
        total_defense = self.defense
        
        # Apply equipment bonuses
        for item in self.equipped.values():
            if item:
                total_damage += item.damage_bonus
                total_defense += item.defense_bonus
                
        return total_damage, total_defense
        
    def add_item(self, item):
        self.inventory.append(item)
        
    def remove_item(self, item):
        self.inventory.remove(item)
        
    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
            return
            
        print("Inventory:")
        for item in self.inventory:
            print(f"- {item}") 
        
    def show_journal(self):
        print("\n=== Journal ===")
        print("1. View Bestiary")
        print("2. View Discovered Locations")
        print("3. View Quest Notes")
        choice = input("What would you like to view? ")
        
        if choice == "1":
            self.journal.show_bestiary()
        elif choice == "2":
            self.journal.show_locations()
        elif choice == "3":
            self.journal.show_quest_notes() 
        
    def update_needs(self):
        # Every 10 minutes
        self.hunger -= 0.5
        self.thirst -= 1.0
        self.energy -= 0.3
        self.bladder -= 0.7
        
        if self.hunger <= 0 or self.thirst <= 0:
            self.health -= 1
            print("You're dying of hunger/thirst!")
        
        if self.energy <= 20:
            print("You're exhausted and need sleep!")
            
        if self.bladder <= 20:
            print("You really need to relieve yourself!") 
        
    def consume_food(self, item):
        if item.type != "food":
            return "That's not edible."
            
        if "raw" in item.name.lower() and "meat" in item.name.lower():
            self.health -= 10
            print("Eating raw meat makes you feel sick!")
            
        self.hunger = min(100, self.hunger + item.food_value)
        self.inventory.remove(item)
        return f"You eat the {item.name}." 
        
    def apply_effect(self, effect):
        effect_name, duration = effect
        self.status_effects[effect_name] = duration
        
    def update_effects(self):
        expired = []
        for effect, turns in self.status_effects.items():
            if effect == "poison":
                self.health -= 2
            elif effect == "bleeding":
                self.health -= 1
            elif effect == "weakness":
                self.damage = int(self.damage * 0.7)
            
            self.status_effects[effect] = turns - 1
            if self.status_effects[effect] <= 0:
                expired.append(effect)
                
        for effect in expired:
            del self.status_effects[effect]
            print(f"The {effect} effect has worn off!") 
        
    def unequip(self, slot):
        if slot in self.equipped and self.equipped[slot]:
            item = self.equipped[slot]
            self.equipped[slot] = None
            self.inventory.append(item)
            return True
        return False 

    @property
    def dodge_chance(self):
        """Calculate dodge chance based on dexterity"""
        base_dodge = self._base_dodge_chance
        dex_bonus = (self.dexterity - 5) * 0.03
        return base_dodge + dex_bonus

    @property
    def max_health(self):
        """Calculate max health based on vitality"""
        base_health = self._base_max_health
        vit_bonus = (self.vitality - 5) * 10  # +10 health per point above 5
        return base_health + vit_bonus 