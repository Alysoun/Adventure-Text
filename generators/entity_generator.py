import random
from entities import Entity
from models.traits import TraitSystem

class EntityGenerator:
    def __init__(self):
        self.trait_system = TraitSystem()
        self.bestiary = {
            "wolf": {
                "variants": ["grey wolf", "timber wolf", "dire wolf"],
                "rare_variants": ["ghost wolf", "alpha dire wolf", "ancient wolf"],
                "behaviors": ["pack", "territorial", "hunter"],
                "stats": {
                    "health": (30, 50),
                    "damage": (5, 12),
                    "defense": (2, 5)
                },
                "rare_stats_multiplier": 2.0,
                "loot_table": ["wolf_pelt", "wolf_fang", "raw_meat"],
                "rare_loot_table": ["spectral_pelt", "alpha_fang", "ancient_rune"],
                "common_traits": [
                    "young",        # Less health but faster
                    "old",         # More experience but slower
                    "scarred",     # Slightly more defense
                    "lone",        # More damage but no pack behavior
                    "hungry",      # More aggressive, less defense
                    "cautious",    # More likely to flee when injured
                    "territorial", # Stronger in its home area
                    "curious"      # Might follow player without attacking
                ],
                "uncommon_traits": [
                    "alpha",       # Can call for pack reinforcements
                    "swift",       # Double movement speed
                    "fierce",      # Critical hit chance increased
                    "cunning",     # Might set up ambushes
                    "stalker",     # Stealth attacks from behind
                    "veteran",     # Immune to status effects
                    "pack-leader", # Buffs nearby allies
                    "battle-worn"  # Regenerates health slowly
                ],
                "rare_traits": [
                    "ethereal",    # Can phase through walls
                    "legendary",   # All stats enhanced
                    "mythical",    # Unique abilities
                    "blessed",     # Divine protection, resistant to damage
                    "cursed",      # Deals damage over time
                    "ancient",     # Can use special abilities
                    "primal",      # Becomes stronger at low health
                    "shadow-touched" # Can teleport short distances
                ],
                "trait_loot_bonus": {
                    "common": 1.0,
                    "uncommon": 1.5,
                    "rare": 2.0
                }
            },
            "bat": {
                "variants": ["cave bat", "vampire bat", "giant bat"],
                "rare_variants": ["shadow bat", "blood lord bat", "elder bat"],
                "behaviors": ["nocturnal", "swarm", "echo"],
                "stats": {
                    "health": (10, 20),
                    "damage": (2, 5),
                    "defense": (1, 2)
                },
                "rare_stats_multiplier": 2.0,
                "loot_table": ["bat_wing", "echo_crystal", "guano"],
                "rare_loot_table": ["shadow_essence", "blood_crystal", "elder_wing"],
                "possible_traits": ["albino", "diseased", "elder"],
                "common_traits": [
                    "small",       # Harder to hit
                    "noisy",       # Gives away position
                    "drowsy",      # Less active during day
                    "alert",       # Better at dodging
                    "frail",       # Less health but more damage
                    "skittish",    # Flees more easily
                    "social",      # Always appears in groups
                    "blind"        # Relies on echolocation
                ],
                "uncommon_traits": [
                    "vampiric",    # Heals when dealing damage
                    "sonic",       # Sound-based attacks
                    "venomous",    # Poisonous attacks
                    "giant",       # Increased size and stats
                    "swarmer",     # Calls more bats
                    "hunter",      # Better tracking ability
                    "screamer",    # Can stun with sonic blast
                    "night-blessed" # Stronger at night
                ],
                "rare_traits": [
                    "blood-lord",  # Creates thralls from defeated enemies
                    "shadow-wing", # Can create darkness
                    "echo-master", # Sonic abilities enhanced
                    "void-touched",# Can create portals
                    "dream-eater", # Causes sleep effects
                    "soul-drinker",# Steals max health
                    "storm-rider", # Controls weather
                    "time-shifted" # Can slow time briefly
                ]
            },
            "troll": {
                "variants": ["cave troll", "bridge troll", "mountain troll"],
                "rare_variants": ["frost troll", "two-headed troll", "troll king"],
                "behaviors": ["territorial", "aggressive", "collector"],
                "stats": {
                    "health": (80, 120),
                    "damage": (15, 25),
                    "defense": (8, 12)
                },
                "rare_stats_multiplier": 2.0,
                "loot_table": ["troll_hide", "gold_pouch", "crude_weapon"],
                "rare_loot_table": ["frost_crystal", "crown_shard", "ancient_gold"],
                "possible_traits": ["ancient", "one-eyed", "regenerating"],
                "common_traits": [
                    "dim",        # Less tactical but more strength
                    "greedy",     # Distracted by treasure
                    "tough",      # More health
                    "sluggish",   # Slower but hits harder
                    "crude",      # Uses improvised weapons
                    "stubborn",   # Resists being moved
                    "loud",       # Gives away position
                    "hungry"      # More aggressive
                ],
                "uncommon_traits": [
                    "regenerating",# Heals over time
                    "armored",    # Natural armor plates
                    "berserker",  # Stronger when injured
                    "boulder-thrower", # Ranged attacks
                    "earth-shaker",# Ground slam attacks
                    "collector",   # Better loot drops
                    "tribal",     # Can call for help
                    "wise"        # Uses tactics
                ],
                "rare_traits": [
                    "frost-touched",# Ice abilities
                    "two-headed",  # Two actions per turn
                    "royal",      # Can command others
                    "ancient",    # Knows magic
                    "mountain-heart",# Cannot be moved
                    "rune-carved", # Magic resistance
                    "world-breaker",# Destroys terrain
                    "titan-blood" # Grows stronger in combat
                ]
            }
        }

    def generate_entity(self, entity_type, level=1, force_rare=False):
        """Generate an entity with random traits and stats"""
        if entity_type not in self.bestiary:
            raise ValueError(f"Unknown entity type: {entity_type}")
            
        template = self.bestiary[entity_type]
        
        # Determine rarity and traits
        is_rare = force_rare or random.random() < 0.05
        
        # Select variant based on rarity
        if is_rare:
            variant = random.choice(template["rare_variants"])
            trait_pool = template["rare_traits"]
            loot_table = template["rare_loot_table"]
            multiplier = template["rare_stats_multiplier"]
        else:
            variant = random.choice(template["variants"])
            # Roll for trait rarity
            trait_roll = random.random()
            if trait_roll < 0.05:  # 5% chance for rare trait
                trait_pool = template["rare_traits"]
                loot_multiplier = template["trait_loot_bonus"]["rare"]
            elif trait_roll < 0.20:  # 15% chance for uncommon trait
                trait_pool = template["uncommon_traits"]
                loot_multiplier = template["trait_loot_bonus"]["uncommon"]
            else:
                trait_pool = template["common_traits"]
                loot_multiplier = template["trait_loot_bonus"]["common"]
            
            loot_table = template["loot_table"]
            multiplier = 1.0
        
        trait = random.choice(trait_pool)
        behavior = random.choice(template["behaviors"])
        
        # Scale stats based on level and rarity
        stats = {
            stat: int(base * multiplier * (1 + 0.1 * level))
            for stat, (base, _) in template["stats"].items()
        }
        
        # Create entity
        entity = Entity(variant, f"A {trait} {variant} that appears {behavior}")
        entity.health = stats["health"]
        entity.damage = stats["damage"]
        entity.defense = stats["defense"]
        entity.behavior = behavior
        entity.trait = trait
        entity.trait_rarity = "rare" if trait in template["rare_traits"] else \
                             "uncommon" if trait in template["uncommon_traits"] else \
                             "common"
        entity.loot_table = loot_table
        entity.loot_multiplier = loot_multiplier if not is_rare else multiplier
        entity.is_rare = is_rare
        
        # Apply trait effects
        self.trait_system.apply_trait(entity, trait)
        
        return entity 