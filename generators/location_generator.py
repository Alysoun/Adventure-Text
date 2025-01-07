from models import Location
import random

class LocationGenerator:
    def __init__(self):
        self.descriptors = {
            "meadow": {
                "features": ["tall grass", "wildflowers", "gentle breeze"],
                "description": "A peaceful meadow stretches before you."
            },
            "forest": {
                "features": ["tall trees", "dense undergrowth", "forest sounds"],
                "description": "A dense forest surrounds you."
            },
            "cave": {
                "features": ["stalactites", "echoing walls", "darkness"],
                "description": "A dark cave opens before you."
            }
        }

    def generate_location(self, location_type):
        """Generate a location of the given type"""
        if location_type not in self.descriptors:
            raise ValueError(f"Unknown location type: {location_type}")
            
        template = self.descriptors[location_type]
        return Location(location_type, template["description"]) 