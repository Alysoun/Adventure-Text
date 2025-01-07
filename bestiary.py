from items import Item

class EntityType:
    def __init__(self, name, description, loot_table=None, hostile=False, 
                 can_talk=False, preferred_food=None, story=None):
        self.name = name
        self.description = description
        self.loot_table = loot_table or []
        self.hostile = hostile
        self.can_talk = can_talk
        self.preferred_food = preferred_food
        self.story = story or "No additional information known."

class Bestiary:
    def __init__(self):
        self.entities = {
            # Neutral entities
            "dead body": EntityType(
                name="dead body",
                description="A lifeless body lies in the grass",
                loot_table=[
                    (Item("gold coins", "A handful of golden coins"), 0.7),
                    (Item("dagger", "A rusty but serviceable dagger"), 0.5),
                    (Item("letter", "A weathered letter with mysterious contents"), 0.3),
                    (Item("brass key", "An ornate brass key"), 0.2),
                    (Item("silver ring", "A silver ring with strange markings"), 0.4)
                ],
                story="""The body appears to be that of a previous adventurer. 
                Their final expression suggests they died in fear rather than from wounds.
                What terrors lurk in these lands?"""
            ),
            
            # Forest creatures
            "wolf": EntityType(
                name="wolf",
                description="A grey wolf watches you cautiously",
                hostile=True,
                preferred_food="meat",
                loot_table=[
                    (Item("wolf fang", "A sharp fang from a wolf"), 0.3),
                    (Item("wolf pelt", "A thick, grey wolf pelt"), 0.5)
                ],
                story="""The wolves in these lands are unusually large and intelligent.
                Local legends speak of an ancient pact between wolves and the first settlers,
                broken by betrayal. Now they trust no human, though some say they can be befriended."""
            ),
            
            # Cave dwellers
            "bat": EntityType(
                name="bat",
                description="A large bat hangs from the ceiling, something glints around its neck",
                preferred_food="fruit",
                loot_table=[
                    (Item("silver chain", "A delicate silver chain, perhaps from a previous adventurer"), 1.0)
                ],
                story="""These aren't ordinary bats - they're descendants of the messenger bats
                used by the ancient cave dwellers. The chains they wear were once used to carry
                messages between underground cities."""
            ),
            
            # Add more entity types as needed...
        }
    
    def get_entity_type(self, name):
        return self.entities.get(name)
    
    def get_all_entries(self):
        return self.entities.items() 