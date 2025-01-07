import os
from colors import Colors

class Display:
    def __init__(self):
        self.width = 80  # Terminal width
        
    def show_location(self, location):
        """Display the current location description"""
        print("\n" + "="*self.width)
        print(f"Location: {location.name}")
        print("="*self.width)
        print(location.get_description())
        
    def show_status(self, game_state):
        """Display player status and time"""
        print("\n" + "-"*self.width)
        health = game_state.player.health
        time = game_state.time.get_time_of_day()
        day = game_state.time.get_day_number()
        
        status = f"Health: {health}% | Time: {time} | Day {day}"
        if game_state.player.status_effects:
            effects = ", ".join(game_state.player.status_effects.keys())
            status += f" | Effects: {effects}"
            
        print(status)
        print("-"*self.width) 
        
    def show_character_sheet(self, stats):
        print("\n=== Character Info ===\n")
        
        # Create a box border
        print("╔" + "═" * (self.width - 2) + "╗")
        
        # Character name and basic info
        print("║ " + Colors.BOLD + "Character Stats" + Colors.RESET + " " * (self.width - 17) + "║")
        print("║" + "─" * (self.width - 2) + "║")
        
        # Basic stats
        health_color = Colors.SUCCESS if stats['health'] > stats['max_health'] * 0.7 else Colors.WARNING
        health_str = f"{stats['health']}/{stats['max_health']}"  # Create the health string separately
        print(f"║ Health: {Colors.colorize(health_str, health_color)}")
        print(f"║ Level: {Colors.colorize(str(stats['level']), Colors.INFO)} (Exp: {stats['exp']})")
        print(f"║ Gold: {Colors.colorize(str(stats['gold']), Colors.LEGENDARY)}")
        print("║")
        
        # Attributes
        print("║ " + Colors.BOLD + "Attributes:" + Colors.RESET)
        for attr, value in stats['attributes'].items():
            color = Colors.COMMON
            if value >= 7:
                color = Colors.RARE
            elif value >= 5:
                color = Colors.UNCOMMON
            print(f"║ {attr + ':':15} {Colors.colorize(str(value), color)}")
        print("║")
        
        # Skills
        print("║ " + Colors.BOLD + "Skills:" + Colors.RESET)
        for skill, level in stats['skills'].items():
            print(f"║ • {skill:20} (Level {Colors.colorize(str(level), Colors.INFO)})")
        
        # Close box
        print("╚" + "═" * (self.width - 2) + "╝") 