import random
from base_classes import Location
from items import Item
from entities import Entity

class LocationGenerator:
    def __init__(self):
        self.descriptors = {
            'meadow': {
                'features': ['wildflowers', 'tall grass', 'small rocks'],
                'sounds': ['birds chirping', 'grass rustling', 'insects buzzing']
            },
            'forest': {
                'features': ['tall trees', 'fallen logs', 'mushrooms'],
                'sounds': ['leaves rustling', 'branches creaking', 'birds calling']
            },
            'cave': {
                'features': ['stalactites', 'glowing crystals', 'rock formations'],
                'sounds': ['water dripping', 'distant echoes', 'wind whistling']
            }
        }
        
    def generate_location(self, location_type):
        """Generate a location of the specified type"""
        if location_type not in self.descriptors:
            return None
            
        desc = self.descriptors[location_type]
        features = random.choice(desc['features'])
        sounds = random.choice(desc['sounds'])
        
        description = f"A {location_type} with {features}. You can hear {sounds}."
        return Location(location_type, description)

class ItemGenerator:
    def __init__(self):
        self.prefixes = {
            "quality": ["crude", "basic", "fine", "masterwork", "legendary"],
            "condition": ["broken", "worn", "pristine", "ancient", "restored"],
            "material": ["iron", "steel", "bronze", "copper", "silver", "crystal", "bone", "wooden"],
            "magical": ["enchanted", "cursed", "blessed", "mystical", "glowing"]
        }
        self.item_types = {
            "weapon": {
                "sword": {"damage": (3, 8), "value": (10, 50)},
                "dagger": {"damage": (2, 5), "value": (5, 25)},
                "axe": {"damage": (4, 9), "value": (12, 55)},
                "spear": {"damage": (3, 7), "value": (8, 40)},
                "mace": {"damage": (4, 8), "value": (10, 45)}
            },
            "armor": {
                "helmet": {"defense": (1, 4), "value": (8, 35)},
                "chestplate": {"defense": (3, 8), "value": (15, 60)},
                "boots": {"defense": (1, 3), "value": (6, 30)},
                "shield": {"defense": (2, 5), "value": (10, 40)}
            },
            "food": {
                "bread": {"food_value": (15, 25), "value": (2, 8)},
                "meat": {"food_value": (25, 40), "value": (4, 12)},
                "fruit": {"food_value": (10, 20), "value": (1, 6)},
                "herbs": {"food_value": (5, 15), "value": (3, 15)}
            }
        }

    def generate_item(self, item_type=None, quality_level=0):
        if not item_type:
            item_type = random.choice(list(self.item_types.keys()))
            
        if item_type == "weapon":
            return self._generate_weapon(quality_level)
        elif item_type == "armor":
            return self._generate_armor(quality_level)
        else:
            return self._generate_food()

    def _generate_weapon(self, quality_level):
        weapon_type = random.choice(list(self.item_types["weapon"].keys()))
        material = random.choice(self.prefixes["material"])
        quality = self._get_quality_prefix(quality_level)
        
        base_stats = self.item_types["weapon"][weapon_type]
        damage = random.randint(*base_stats["damage"]) + quality_level
        
        name = f"{quality} {material} {weapon_type}"
        desc = f"A {quality.lower()} {weapon_type} made of {material}"
        
        # Determine rarity based on quality level
        rarity = Item.COMMON
        if quality_level >= 4:
            rarity = Item.LEGENDARY
        elif quality_level >= 3:
            rarity = Item.EPIC
        elif quality_level >= 2:
            rarity = Item.RARE
        elif quality_level >= 1:
            rarity = Item.UNCOMMON
        
        return Item(name, desc, "weapon", rarity=rarity, damage_bonus=damage)

    def _get_quality_prefix(self, quality_level):
        if quality_level <= 1:
            return random.choice(self.prefixes["quality"][:2])
        elif quality_level <= 3:
            return random.choice(self.prefixes["quality"][1:4])
        else:
            return random.choice(self.prefixes["quality"][3:])

    def _generate_food(self):
        food_type = random.choice(list(self.item_types["food"].keys()))
        quality = self._get_quality_prefix(random.randint(0, 2))
        
        base_stats = self.item_types["food"][food_type]
        food_value = random.randint(*base_stats["food_value"])
        
        # Some foods start raw and need cooking
        if food_type == "meat":
            name = f"raw {food_type}"
            desc = f"Raw {food_type} that should be cooked before eating"
            food_value *= 0.5  # Raw food is less nutritious and might be dangerous
        else:
            name = f"{quality} {food_type}"
            desc = f"A {quality.lower()} portion of {food_type}"
        
        return Item(name, desc, "food", food_value=food_value)

    def _generate_armor(self, quality_level=0):
        armor_type = random.choice(list(self.item_types["armor"].keys()))
        material = random.choice(self.prefixes["material"])
        quality = self._get_quality_prefix(quality_level)
        
        base_stats = self.item_types["armor"][armor_type]
        defense = random.randint(*base_stats["defense"]) + quality_level
        
        name = f"{quality} {material} {armor_type}"
        desc = f"A {quality.lower()} {armor_type} made of {material}"
        
        return Item(name, desc, "armor", defense_bonus=defense)

    def generate_item_by_name(self, item_name):
        """Generate an item with a specific name"""
        # Parse the item name to determine type and properties
        name_parts = item_name.lower().split()
        
        # Handle special items first
        if "note" in name_parts:
            return Item(
                name="mysterious note", 
                description="An old parchment with elegant script",
                item_type=Item.QUEST_ITEM
            )
            
        # Handle weapons
        if any(weapon in name_parts for weapon in self.item_types["weapon"]):
            weapon_type = next(w for w in self.item_types["weapon"] if w in name_parts)
            quality = next((p for p in self.prefixes["quality"] if p in name_parts), "basic")
            material = next((m for m in self.prefixes["material"] if m in name_parts), "iron")
            
            base_stats = self.item_types["weapon"][weapon_type]
            damage = sum(base_stats["damage"]) // 2  # Use average damage
            
            name = f"{quality} {material} {weapon_type}"
            desc = f"A {quality.lower()} {weapon_type} made of {material}"
            return Item(name, desc, "weapon", damage_bonus=damage)
            
        # Handle armor
        if any(armor in name_parts for armor in self.item_types["armor"]):
            armor_type = next(a for a in self.item_types["armor"] if a in name_parts)
            quality = next((p for p in self.prefixes["quality"] if p in name_parts), "basic")
            material = next((m for m in self.prefixes["material"] if m in name_parts), "iron")
            
            base_stats = self.item_types["armor"][armor_type]
            defense = sum(base_stats["defense"]) // 2  # Use average defense
            
            name = f"{quality} {material} {armor_type}"
            desc = f"A {quality.lower()} {armor_type} made of {material}"
            return Item(name, desc, "armor", defense_bonus=defense)
            
        # Handle food
        if any(food in name_parts for food in self.item_types["food"]):
            food_type = next(f for f in self.item_types["food"] if f in name_parts)
            quality = next((p for p in self.prefixes["quality"] if p in name_parts), "basic")
            
            base_stats = self.item_types["food"][food_type]
            food_value = sum(base_stats["food_value"]) // 2  # Use average food value
            
            if "raw" in name_parts and food_type == "meat":
                name = f"raw {food_type}"
                desc = f"Raw {food_type} that should be cooked before eating"
                food_value *= 0.5
            else:
                name = f"{quality} {food_type}"
                desc = f"A {quality.lower()} portion of {food_type}"
                
            return Item(name, desc, "food", food_value=food_value)
            
        # If we can't determine the item type, return None
        return None

class EntityGenerator:
    def __init__(self):
        self.types = {
            "hostile": {
                "wolf": {"health": (25, 35), "damage": (6, 10), "defense": (1, 3)},
                "bandit": {"health": (30, 40), "damage": (8, 12), "defense": (2, 4)},
                "spider": {"health": (20, 30), "damage": (5, 8), "defense": (1, 2)},
                "skeleton": {"health": (25, 35), "damage": (7, 11), "defense": (1, 3)}
            },
            "neutral": {
                "merchant": {"health": (20, 25), "damage": (3, 5), "defense": (1, 2)},
                "traveler": {"health": (25, 30), "damage": (4, 6), "defense": (1, 2)},
                "hermit": {"health": (20, 25), "damage": (3, 5), "defense": (1, 2)}
            },
            "passive": {
                "rabbit": {"health": (10, 15), "damage": (1, 2), "defense": (0, 1)},
                "deer": {"health": (15, 20), "damage": (2, 3), "defense": (0, 1)},
                "bird": {"health": (8, 12), "damage": (1, 2), "defense": (0, 1)}
            }
        }

    def generate_entity(self, entity_type=None, disposition=None):
        if not disposition:
            disposition = random.choice(list(self.types.keys()))
        if not entity_type:
            entity_type = random.choice(list(self.types[disposition].keys()))
            
        stats = self.types[disposition][entity_type]
        health = random.randint(*stats["health"])
        damage = random.randint(*stats["damage"])
        defense = random.randint(*stats["defense"])
        
        entity = Entity(entity_type, self._generate_description(entity_type, disposition))
        entity.health = health
        entity.damage = damage
        entity.defense = defense
        entity.hostile = (disposition == "hostile")
        
        return entity

    def _generate_description(self, entity_type, disposition):
        descriptions = {
            "hostile": {
                "wolf": ["A fierce wolf with gleaming eyes", "A snarling wolf bares its teeth"],
                "bandit": ["A rough-looking bandit eyes you suspiciously", "A armed bandit watches your movements"],
                "spider": ["A large spider moves in the shadows", "A menacing spider clicks its mandibles"],
                "skeleton": ["A skeletal warrior clutches ancient weapons", "A animated skeleton stands guard"]
            },
            "neutral": {
                "merchant": ["A traveling merchant with a heavy pack", "A weary merchant rests here"],
                "traveler": ["A fellow traveler pauses on their journey", "A mysterious traveler considers you"],
                "hermit": ["A solitary hermit keeps to themselves", "A wise-looking hermit meditates quietly"]
            },
            "passive": {
                "rabbit": ["A small rabbit nibbles on plants", "A cautious rabbit watches you"],
                "deer": ["A graceful deer grazes nearby", "A alert deer raises its head"],
                "bird": ["A colorful bird perches nearby", "A small bird hops around"]
            }
        }
        return random.choice(descriptions[disposition][entity_type]) 

class RewardGenerator:
    def __init__(self):
        self.reward_tiers = {
            "basic": {
                "items": ["healing_potion", "bread", "torch"],
                "quality_range": (0, 1),
                "quantity_range": (1, 2)
            },
            "intermediate": {
                "items": ["weapon", "armor", "magic_crystal"],
                "quality_range": (2, 3),
                "quantity_range": (1, 3)
            },
            "advanced": {
                "items": ["rare_weapon", "rare_armor", "ancient_artifact"],
                "quality_range": (3, 4),
                "quantity_range": (2, 3)
            }
        }

    def generate_reward(self, tier, item_generator):
        tier_data = self.reward_tiers[tier]
        rewards = []
        
        quantity = random.randint(*tier_data["quality_range"])
        quality = random.randint(*tier_data["quality_range"])
        
        for _ in range(quantity):
            if "weapon" in tier_data["items"]:
                rewards.append(item_generator.generate_item("weapon", quality_level=quality))
            elif "armor" in tier_data["items"]:
                rewards.append(item_generator.generate_item("armor", quality_level=quality))
            else:
                item_type = random.choice(tier_data["items"])
                rewards.append(item_generator.generate_item(item_type, quality_level=quality))
                
        return rewards 