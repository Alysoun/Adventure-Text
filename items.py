from colors import Colors

class Item:
    # Define standard item types as class variables
    WEAPON = "weapon"
    ARMOR = "armor"
    FOOD = "food"
    QUEST_ITEM = "quest_item"
    MISC = "misc"
    
    # Define rarities
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"
    UNIQUE = "unique"
    QUEST = "quest"
    
    # Map rarities to colors
    RARITY_COLORS = {
        COMMON: Colors.COMMON,
        UNCOMMON: Colors.UNCOMMON,
        RARE: Colors.RARE,
        EPIC: Colors.EPIC,
        LEGENDARY: Colors.LEGENDARY,
        MYTHIC: Colors.MYTHIC,
        UNIQUE: Colors.UNIQUE,
        QUEST: Colors.QUEST
    }
    
    def __init__(self, name, description, item_type, rarity=COMMON, **kwargs):
        """
        Initialize an item
        
        Args:
            name (str): Name of the item
            description (str): Basic description
            item_type (str): Type of item (weapon/armor/food/quest_item/misc)
            rarity (str): Rarity of the item
            **kwargs: Additional properties like damage_bonus, defense_bonus, food_value
        """
        self.name = name
        self.description = description
        self.type = item_type
        self.rarity = rarity
        self.examine_text = None
        
        # Set additional properties from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        # Initialize default values
        if not hasattr(self, 'damage_bonus'):
            self.damage_bonus = 0
        if not hasattr(self, 'defense_bonus'):
            self.defense_bonus = 0
        if not hasattr(self, 'food_value'):
            self.food_value = 0
        
    def examine(self, game_state=None):
        """Return detailed examination text for the item"""
        if game_state and self.name.lower() == "mysterious note":
            item_info = game_state.story.get_item_description(self.name)
            if item_info:
                return item_info["examine_text"]
                
        return self.description
        
    def __str__(self):
        """Return colored item name based on rarity"""
        color = self.RARITY_COLORS.get(self.rarity, Colors.COMMON)
        return Colors.colorize(self.name, color)
        
    def use(self, player):
        if self.type == "food":
            player.hunger += self.food_value
            return f"You eat the {self.name}. Hunger restored by {self.food_value}!"
        elif self.use_effect:
            return self.use_effect(player) 