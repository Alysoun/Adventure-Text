class Item:
    def __init__(self, name, description, type, damage_bonus=0, defense_bonus=0, weight=1):
        self.name = name
        self.description = description
        self.type = type
        self.damage_bonus = damage_bonus
        self.defense_bonus = defense_bonus
        self.weight = weight
        self.stackable = type in ["food", "potion", "material"] 