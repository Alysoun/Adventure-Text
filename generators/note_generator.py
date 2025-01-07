import random
import string

class NoteGenerator:
    def __init__(self):
        self.templates = {
            "journal": [
                "Day {day}: {event}. The {creature} seemed {behavior}.",
                "Found {item} near the {location}. Must remember to {action}.",
                "Warning: {danger} ahead. Need to {preparation}."
            ],
            "lore": [
                "The ancient {civilization} spoke of {artifact} that could {power}.",
                "Legends tell of {creature} that guard the {location}.",
                "The {ritual} must be performed under {condition}."
            ]
        }
        
        self.content = {
            "event": ["strange lights appeared", "heard mysterious sounds"],
            "creature": ["wolves", "trolls", "bats", "ancient guardian"],
            "behavior": ["unusually aggressive", "strangely calm", "watching"],
            "item": ["glowing crystal", "ancient scroll", "mysterious device"],
            "location": ["dark cave", "abandoned mine", "crystal formation"],
            "action": ["return at night", "bring offerings", "mark on map"],
            "danger": ["unstable caves", "hostile creatures", "dark magic"],
            "preparation": ["gather supplies", "find shelter", "seek help"]
        }

        self.content.update({
            "civilization": ["crystal dwellers", "ancient ones", "forgotten tribe"],
            "artifact": ["crystal heart", "ancient tome", "mystic orb"],
            "power": ["control time", "speak to spirits", "command elements"],
            "ritual": ["crystal binding", "spirit calling", "elemental fusion"],
            "condition": ["full moon", "crystal alignment", "spirit presence"]
        })

    def generate_note(self, note_type="journal", day=1):
        """Generate a random note based on type"""
        if note_type == "journal":
            # Always use first template for journal to ensure day is included
            template = self.templates["journal"][0]
        else:
            template = random.choice(self.templates[note_type])
        
        # Get required keys from template
        required_keys = [k[1] for k in string.Formatter().parse(template) if k[1]]
        
        # Ensure all required keys are available
        content = {"day": day}
        for key in required_keys:
            if key == "day":
                continue
            if key not in self.content:
                content[key] = "unknown"
            else:
                content[key] = random.choice(self.content[key])
            
        # For journal entries, ensure we have event and creature
        if note_type == "journal":
            content["event"] = random.choice(self.content["event"])
            content["creature"] = random.choice(self.content["creature"])
            content["behavior"] = random.choice(self.content["behavior"])
        
        return template.format(**content) 