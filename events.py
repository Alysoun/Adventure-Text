import random

class EventManager:
    def __init__(self):
        self.events = {
            'dawn': [
                ('wolf_howl', "You hear distant wolf howls as the sun rises", (5, 7)),
                ('bird_song', "Birds begin their morning songs", (4, 8))
            ],
            'day': [
                ('merchant', "A traveling merchant appears", (9, 17)),
                ('butterfly', "Colorful butterflies flutter nearby", (10, 16))
            ],
            'dusk': [
                ('bat_swarm', "Bats emerge from the caves", (18, 20)),
                ('sunset', "The setting sun casts long shadows", (17, 19))
            ],
            'night': [
                ('ghost', "A ghostly figure appears in the distance", (22, 4)),
                ('owl', "An owl hoots somewhere in the darkness", (20, 4))
            ]
        }
        
    def check_events(self, game_state):
        hour = (game_state.time.minutes // 60) % 24
        location_type = game_state.current_location.location_type
        
        # Check time-specific events
        for time_of_day, events in self.events.items():
            for event_id, message, (start_hour, end_hour) in events:
                if self._is_time_between(hour, start_hour, end_hour):
                    if random.random() < 0.3:  # 30% chance of event occurring
                        if self._is_event_valid(event_id, location_type):
                            return message
        return None
        
    def _is_time_between(self, hour, start, end):
        if start <= end:
            return start <= hour < end
        else:  # Handles overnight events (e.g., 22-4)
            return hour >= start or hour < end
            
    def _is_event_valid(self, event_id, location_type):
        # Check if event makes sense for location
        if event_id == 'bat_swarm' and location_type != 'cave':
            return False
        if event_id == 'butterfly' and location_type == 'cave':
            return False
        return True 