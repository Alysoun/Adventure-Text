class TraitEffect:
    def __init__(self, name, description, stat_modifiers=None, abilities=None):
        self.name = name
        self.description = description
        self.stat_modifiers = stat_modifiers or {}
        self.abilities = abilities or []

class TraitSystem:
    def __init__(self):
        self.trait_effects = {
            # Wolf traits
            "alpha": TraitEffect(
                "Alpha",
                "Can call for pack reinforcements",
                stat_modifiers={"damage": 1.2},
                abilities=["call_pack"]
            ),
            "swift": TraitEffect(
                "Swift",
                "Double movement speed",
                stat_modifiers={"speed": 2.0, "dodge_chance": 1.5}
            ),
            "hungry": TraitEffect(
                "Hungry",
                "More aggressive, less defense",
                stat_modifiers={"damage": 1.3, "defense": 0.7, "aggression": 2.0}
            ),

            # Bat traits
            "vampiric": TraitEffect(
                "Vampiric",
                "Heals when dealing damage",
                abilities=["life_drain"]
            ),
            
            # Troll traits
            "berserker": TraitEffect(
                "Berserker",
                "Gets stronger when injured",
                abilities=["rage"]
            ),
        }

    def apply_trait(self, entity, trait_name):
        """Apply a trait's effects to an entity"""
        if trait_name not in self.trait_effects:
            return

        effect = self.trait_effects[trait_name]
        
        # Apply stat modifiers
        for stat, modifier in effect.stat_modifiers.items():
            current_value = getattr(entity, stat, 0)
            setattr(entity, stat, current_value * modifier)
        
        # Add abilities
        entity.abilities.extend(effect.abilities) 