class StoryManager:
    def __init__(self):
        self.quest_stages = {
            "tutorial": 0,
            "wolves": 0,
            "crystals": 0,
            "ancient_secret": 0
        }
        
        self.discovered_chapters = set()
        
        self.quests = {
            "survival": {
                "title": "Learning to Survive",
                "description": "Learn the basics of survival",
                "stages": ["Find food", "Make camp", "Craft tools"],
                "rewards": ["basic_supplies", "survival_knowledge"],
                "chapter": "beginning"
            },
            "wolves": {
                "title": "The Wolf Pack",
                "description": "Gain the trust of the local wolves",
                "stages": ["Find the pack", "Feed the wolves", "Earn trust"],
                "rewards": ["wolf_companion", "hunting_skills"],
                "chapter": "wilderness"
            },
            "crystals": {
                "title": "Crystal Mysteries",
                "description": "Discover the secret of the glowing crystals",
                "stages": ["Find crystals", "Study patterns", "Unlock power"],
                "rewards": ["crystal_shard", "ancient_knowledge"],
                "chapter": "mysteries"
            }
        }
        
        self.flags = {}
        self.active_paths = set()
        
    def check_progress(self, game_state, action, context):
        """Check if an action triggers story progression"""
        updates = []
        
        if action == "enter_location":
            if context["location_type"] == "cave" and not game_state.milestones["cave_discovered"]:
                game_state.milestones["cave_discovered"] = True
                updates.append("You've discovered your first cave!")
                self.quest_stages["crystals"] += 1
                self.discovered_chapters.add("mysteries")
                
        elif action == "interact_entity":
            if context["entity_type"] == "wolf" and context["interaction"] == "feed":
                if not game_state.milestones["wolves_befriended"]:
                    game_state.milestones["wolves_befriended"] = True
                    updates.append("You've gained the wolves' trust!")
                    self.quest_stages["wolves"] += 1
                    self.discovered_chapters.add("wilderness")
                    
        return "\n".join(updates) if updates else None 
        
    def get_opening_text(self):
        """Return the game's opening text"""
        return """
Welcome to Crystal Whispers...

You awaken in a peaceful meadow, your head foggy with half-remembered dreams.
The gentle rustling of grass and distant bird calls fill the air. Nearby,
you notice a mysterious note on the ground, its edges stained with what appears 
to be blood.

Your journey begins here, but where it leads... only the crystals know.

=== Basic Commands ===
- look : examine your surroundings
- take note : pick up the mysterious note
- inventory : check your belongings
- help : show all commands
""" 
        
    def get_initial_note_text(self):
        """Return the text of the mysterious note found at the start"""
        return """
The ancient crystals in these caves hold a power beyond imagination.
But beware - they are guarded by those who have forgotten their true purpose.

The wolves remember the old ways. Gain their trust, and they will guide you.
The bats carry messages between the sacred places. Feed them, and they may share their secrets.

Be cautious, be kind, and above all - listen to the crystal whispers.

- A Friend
"""
        
    def get_item_description(self, item_name):
        """Get special descriptions for story-related items"""
        if item_name.lower() == "mysterious note":
            return {
                "name": "Mysterious Note",
                "description": "An old parchment with elegant script, stained with blood",
                "examine_text": self.get_initial_note_text()
            }
            
        # Add other special items here
        return None 
        
    def set_flag(self, flag_name, value):
        """Set a story flag"""
        self.flags[flag_name] = value
        
    def get_flag(self, flag_name):
        """Get a story flag value"""
        return self.flags.get(flag_name, False)
        
    def complete_quest(self, quest_name):
        """Mark a quest as complete"""
        if quest_name in self.quest_stages:
            self.quest_stages[quest_name] = 100  # 100% complete
            return True
        return False
        
    def add_quest(self, quest_id, description, target=1):
        """Add a new quest"""
        self.quest_stages[quest_id] = 0
        
    def is_quest_complete(self, quest_id):
        """Check if a quest is complete"""
        return self.quest_stages.get(quest_id, 0) >= 100
        
    def choose_path(self, path):
        """Choose a story path"""
        self.active_paths.add(path) 