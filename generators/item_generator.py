import random
from items import Item

class ItemGenerator:
    def __init__(self):
        self.prefixes = {
            "weapon": ["Sharp", "Rusty", "Ancient", "Blessed", "Cursed"],
            "armor": ["Sturdy", "Worn", "Enchanted", "Heavy", "Light"],
            "accessory": ["Glowing", "Mysterious", "Powerful", "Delicate"],
            "quest_item": ["Ancient", "Mysterious", "Sacred", "Lost"]
        }
        
        self.materials = {
            "weapon": ["Iron", "Steel", "Bronze", "Crystal", "Bone"],
            "armor": ["Leather", "Chain", "Plate", "Hide", "Scale"],
            "accessory": ["Silver", "Gold", "Wood", "Stone", "Crystal"],
            "quest_item": ["Crystal", "Scroll", "Relic", "Artifact"]
        }
        
        self.item_types = {
            "weapon": {
                "sword": {"damage": (5, 10), "weight": 5},
                "axe": {"damage": (7, 12), "weight": 7},
                "spear": {"damage": (4, 8), "weight": 4}
            },
            "armor": {
                "chest": {"defense": (3, 8), "weight": 8},
                "helmet": {"defense": (2, 5), "weight": 3},
                "boots": {"defense": (1, 3), "weight": 2}
            },
            "quest_item": {
                "key": {"weight": 1},
                "scroll": {"weight": 1},
                "artifact": {"weight": 2}
            }
        }

    def generate_item(self, category, quality=0):
        """Generate a random item of given category and quality"""
        if category not in self.prefixes:
            return None  # Return None for unknown categories
        
        prefix = random.choice(self.prefixes[category])
        material = random.choice(self.materials[category])
        item_type = random.choice(list(self.item_types[category].keys()))
        
        base_stats = self.item_types[category][item_type]
        name = f"{prefix} {material} {item_type}"
        
        if category in ["weapon", "armor"]:
            # Handle combat items as before
            return self._generate_combat_item(category, name, base_stats, quality)
        else:
            # Handle other item types
            return Item(name, f"A {name.lower()}", category, weight=base_stats["weight"])

    def generate_item_by_name(self, name):
        """Generate a specific item by name"""
        # Parse name format: "{prefix} {material} {type}"
        parts = name.split()
        if len(parts) != 3:
            return None
        
        prefix, material, item_type = parts
        category = next((cat for cat, types in self.item_types.items() 
                        if item_type in types), None)
                        
        if not category:
            return None
        
        return self.generate_item(category) 

    def _generate_combat_item(self, category, name, base_stats, quality=0):
        """Helper method to generate combat items (weapons/armor)"""
        stat_bonus = quality * 2  # More significant quality impact
        
        if category == "weapon":
            damage = base_stats["damage"][0] + stat_bonus  # Use base damage + quality bonus
            return Item(name, f"A {name.lower()}", category, 
                       damage_bonus=damage, weight=base_stats["weight"])
                   
        elif category == "armor":
            defense = base_stats["defense"][0] + stat_bonus  # Use base defense + quality bonus
            return Item(name, f"A {name.lower()}", category,
                       defense_bonus=defense, weight=base_stats["weight"]) 