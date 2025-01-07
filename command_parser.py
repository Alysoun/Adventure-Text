from commands import (LookCommand, SearchCommand, MoveCommand, 
                     InventoryCommand, TakeCommand, DropCommand, 
                     ExamineCommand, HelpCommand, AttackCommand, 
                     TalkCommand, FeedCommand, SurveyCommand, 
                     CampCommand, EatCommand, DrinkCommand,
                     EquipCommand, UnequipCommand, EquipmentCommand,
                     QuestCommand, AchievementsCommand, StatsCommand)

class CommandParser:
    def __init__(self):
        self.commands = {
            # Basic commands and aliases
            'look': LookCommand,
            'l': LookCommand,
            'examine': ExamineCommand,
            'read': ExamineCommand,
            'inspect': ExamineCommand,
            'check': ExamineCommand,
            'x': ExamineCommand,
            
            # Movement commands
            'go': MoveCommand,
            'move': MoveCommand,
            'walk': MoveCommand,
            'run': MoveCommand,
            'n': lambda args: MoveCommand(['north']),
            's': lambda args: MoveCommand(['south']),
            'e': lambda args: MoveCommand(['east']),
            'w': lambda args: MoveCommand(['west']),
            
            # Inventory commands
            'inventory': InventoryCommand,
            'i': InventoryCommand,
            'inv': InventoryCommand,
            'items': InventoryCommand,
            'bag': InventoryCommand,
            
            # Item interaction
            'take': TakeCommand,
            'get': TakeCommand,
            'grab': TakeCommand,
            'pick': TakeCommand,
            'pickup': TakeCommand,
            'drop': DropCommand,
            'discard': DropCommand,
            'throw': DropCommand,
            
            # Equipment commands
            'equip': EquipCommand,
            'wear': EquipCommand,
            'wield': EquipCommand,
            'put': EquipCommand,
            'unequip': UnequipCommand,
            'remove': UnequipCommand,
            'unwield': UnequipCommand,
            'equipment': EquipmentCommand,
            'gear': EquipmentCommand,
            'stats': EquipmentCommand,
            'eq': EquipmentCommand,
            
            # Interaction commands
            'talk': TalkCommand,
            'speak': TalkCommand,
            'chat': TalkCommand,
            'attack': AttackCommand,
            'fight': AttackCommand,
            'hit': AttackCommand,
            'feed': FeedCommand,
            'give': FeedCommand,
            
            # Environment commands
            'survey': SurveyCommand,
            'scan': SurveyCommand,
            'search': SearchCommand,
            'look around': SurveyCommand,
            
            # Survival commands
            'camp': CampCommand,
            'rest': CampCommand,
            'sleep': CampCommand,
            'make camp': CampCommand,
            'set camp': CampCommand,
            'eat': EatCommand,
            'consume': EatCommand,
            'taste': EatCommand,
            'drink': DrinkCommand,
            'sip': DrinkCommand,
            
            # Information commands
            'help': HelpCommand,
            'h': HelpCommand,
            '?': HelpCommand,
            'quests': QuestCommand,
            'q': QuestCommand,
            'missions': QuestCommand,
            'achievements': AchievementsCommand,
            'ach': AchievementsCommand,
            'a': AchievementsCommand,
            
            # Character commands
            'stats': StatsCommand,
            'character': StatsCommand,
            'char': StatsCommand,
            'c': StatsCommand
        }
        
        # Common phrases to strip out
        self.filler_words = ['the', 'a', 'an', 'at', 'to', 'with', 'using', 'from']
        
    def parse(self, user_input):
        words = user_input.split()
        if not words:
            return None
            
        # Check for multi-word commands first
        for cmd_len in range(2, 0, -1):  # Try 2-word commands, then 1-word
            if len(words) >= cmd_len:
                potential_cmd = ' '.join(words[:cmd_len]).lower()
                if potential_cmd in self.commands:
                    # Remove command words and filler words from args
                    args = [w for w in words[cmd_len:] 
                           if w.lower() not in self.filler_words]
                    return self.commands[potential_cmd](args)
        
        # If no multi-word command found, try single word
        command_word = words[0].lower()
        if command_word in self.commands:
            # Remove filler words from args
            args = [w for w in words[1:] 
                   if w.lower() not in self.filler_words]
            return self.commands[command_word](args)
            
        return None 