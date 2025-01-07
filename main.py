from game_state import GameState
from command_parser import CommandParser
from player import Player
from display import Display
from story import StoryManager
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_welcome():
    clear_screen()
    print("""
╔══════════════════════════════════════════════════════════════╗
║                     Crystal Whispers                         ║
║                                                              ║
║                 A Text Adventure Game                        ║
╚══════════════════════════════════════════════════════════════╝
""")

def main():
    # Initialize game components
    player = Player()
    game_state = GameState(player)
    command_parser = CommandParser()
    display = Display()
    
    # Show welcome screen
    show_welcome()
    print(game_state.story.get_opening_text())
    input("\nPress Enter to begin...")
    
    while True:
        clear_screen()
        
        # Show current location and status
        display.show_location(game_state.current_location)
        display.show_status(game_state)
        
        # Get and process user input
        try:
            user_input = input("\nWhat would you like to do? ").strip().lower()
            
            if user_input == "quit":
                if confirm_quit():
                    break
                continue
                
            command = command_parser.parse(user_input)
            if command:
                command.execute(game_state)
                if user_input == "help":
                    input("\nPress Enter to return to game...")
                else:
                    input("\nPress Enter to continue...")
            else:
                print("I don't understand that command. Type 'help' for a list of commands.")
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            if confirm_quit():
                break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            input("Press Enter to continue...")
    
    # Show exit message
    clear_screen()
    print("Thanks for playing Crystal Whispers!")

def confirm_quit():
    """Ask for confirmation before quitting"""
    response = input("\nAre you sure you want to quit? (y/n) ").strip().lower()
    return response == 'y'

if __name__ == "__main__":
    main() 