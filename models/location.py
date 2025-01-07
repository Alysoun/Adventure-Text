class Location:
    def __init__(self, location_type, description):
        self.location_type = location_type
        self.description = description
        self.entities = []
        self.items = []
        self.connections = {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        }

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_item(self, item):
        self.items.append(item)

    def get_detailed_survey(self):
        return self.description 