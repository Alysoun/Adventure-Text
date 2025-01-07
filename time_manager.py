class TimeManager:
    def __init__(self):
        self.current_time = 0  # Time in minutes
        self.minutes_per_action = 10
        self.minutes_per_day = 1440  # 24 hours * 60 minutes
        
    def advance_time(self, minutes):
        """Advance time by specified minutes. Returns True if a new day starts"""
        old_day = self.current_time // self.minutes_per_day
        self.current_time += minutes
        new_day = self.current_time // self.minutes_per_day
        
        return new_day > old_day
        
    def get_time_of_day(self):
        """Get the current time of day as a string"""
        minutes_today = self.current_time % self.minutes_per_day
        hours = minutes_today // 60
        minutes = minutes_today % 60
        
        if hours < 6:
            return "Night"
        elif hours < 12:
            return "Morning"
        elif hours < 18:
            return "Afternoon"
        else:
            return "Evening"
            
    def get_formatted_time(self):
        """Get the current time formatted as HH:MM"""
        minutes_today = self.current_time % self.minutes_per_day
        hours = minutes_today // 60
        minutes = minutes_today % 60
        return f"{hours:02d}:{minutes:02d}"
        
    def get_day_number(self):
        """Get the current day number"""
        return self.current_time // self.minutes_per_day + 1 