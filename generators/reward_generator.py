import random
from items import Item

class RewardGenerator:
    def __init__(self):
        self.reward_tiers = {
            "basic": {"min_items": 1, "max_items": 2, "quality": (0, 2)},
            "intermediate": {"min_items": 2, "max_items": 3, "quality": (2, 4)},
            "advanced": {"min_items": 2, "max_items": 4, "quality": (4, 6)}
        }

    def generate_reward(self, tier, item_generator):
        """Generate rewards based on tier"""
        if tier not in self.reward_tiers:
            raise ValueError(f"Unknown reward tier: {tier}")
            
        tier_info = self.reward_tiers[tier]
        num_items = random.randint(tier_info["min_items"], tier_info["max_items"])
        quality = random.randint(*tier_info["quality"])
        
        rewards = []
        for _ in range(num_items):
            item_type = random.choice(["weapon", "armor"])
            rewards.append(item_generator.generate_item(item_type, quality))
            
        return rewards 