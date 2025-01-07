class Colors:
    # Basic colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Item rarity colors
    COMMON = '\033[37m'      # White
    UNCOMMON = '\033[32m'    # Green
    RARE = '\033[34m'        # Blue
    EPIC = '\033[35m'        # Purple
    LEGENDARY = '\033[33m'   # Yellow
    MYTHIC = '\033[31m'      # Red
    UNIQUE = '\033[95m'      # Pink
    QUEST = '\033[36m'       # Cyan/Turquoise
    
    # Other useful colors
    WARNING = '\033[93m'     # Yellow
    ERROR = '\033[91m'       # Red
    SUCCESS = '\033[92m'     # Green
    INFO = '\033[94m'        # Blue
    
    @staticmethod
    def colorize(text, color, bold=False):
        """Add color and optionally bold to text"""
        if bold:
            return f"{Colors.BOLD}{color}{text}{Colors.RESET}"
        return f"{color}{text}{Colors.RESET}" 