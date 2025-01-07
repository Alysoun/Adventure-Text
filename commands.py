from items import Item


class Command:
    def __init__(self, args):
        self.args = args
        
    def execute(self, game_state):
        pass

class LookCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print(game_state.current_location.get_description())
            return
            
        direction = self.args[0].lower()
        if direction in ['north', 'south', 'east', 'west']:
            game_state.current_location.look_direction(direction)
        else:
            print("You can only look north, south, east, or west.")

class SearchCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to search?")
            return
            
        target = ' '.join(self.args)
        game_state.current_location.search(target, game_state)

class MoveCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("Which direction would you like to move?")
            return
            
        direction = self.args[0].lower()
        if direction in ['north', 'south', 'east', 'west']:
            game_state.current_location.move_direction(direction, game_state)
        else:
            print("You can only move north, south, east, or west.")

class InventoryCommand(Command):
    def execute(self, game_state):
        game_state.player.show_inventory() 

class TakeCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to take?")
            return
            
        item_name = ' '.join(self.args)
        location = game_state.current_location
        
        for item in location.items:
            if item_name.lower() in item.name.lower():
                location.remove_item(item)
                game_state.player.add_item(item)
                print(f"You took the {item.name}.")
                return
                
        print(f"There is no {item_name} here to take.")

class DropCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to drop?")
            return
            
        item_name = ' '.join(self.args)
        player = game_state.player
        
        for item in player.inventory:
            if item_name.lower() in item.name.lower():
                player.remove_item(item)
                game_state.current_location.add_item(item)
                print(f"You dropped the {item.name}.")
                return
                
        print(f"You don't have a {item_name} to drop.")

class ExamineCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to examine?")
            return
            
        target = ' '.join(self.args).lower()  # Join args into a single string
        
        # Check inventory
        for item in game_state.player.inventory:
            if target in item.name.lower():
                print(f"\n=== {item.name} ===")
                print(item.examine(game_state))
                return
                
        # Check current location
        if game_state.current_location:
            for item in game_state.current_location.items:
                if target in item.name.lower():
                    print(f"\n=== {item.name} ===")
                    print(item.examine(game_state))
                    return
                    
        print(f"You don't see any {target} to examine.")

class HelpCommand(Command):
    def execute(self, game_state):
        print("""
=== Basic Commands ===
- look (l) : examine your surroundings
- examine/read/inspect (x) : look at something closely
- go/move/walk <direction> : move in a direction (n/s/e/w)
- take/get/grab : pick up an item
- inventory (i/inv) : check your belongings
- help (h/?) : show this help message

=== Interaction Commands ===
- search/scan : search something in the area
- talk/speak/chat : attempt to talk to something
- attack/fight/hit : attempt to attack something
- feed/give : try to feed something with an item

=== Equipment Commands ===
- equip/wear/wield : equip an item
- unequip/remove : remove equipped item
- equipment/gear (eq) : check your equipment and stats

=== Survival Commands ===
- eat/taste <food> : consume food items
- drink/sip : drink water if you have it
- cook/prepare : set up camp and cook food
- rest : recover energy when safe
- camp : set up camp for cooking and resting
- status : check your health and needs

=== Information Commands ===
- survey : carefully examine your surroundings
- time : check current time and day
- journal : view your collected information

=== System Commands ===
- save [filename] : save your game
- load [filename] : load a saved game
- quit : exit the game
        """)
        return True 

class AttackCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to attack?")
            return
            
        target = ' '.join(self.args)
        location = game_state.current_location
        player = game_state.player
        
        for entity in location.entities:
            if target.lower() in entity.name.lower():
                damage, defense = player.get_stats()
                result = entity.combat_round(damage, game_state)
                if result.get('player_damage'):
                    final_damage = max(0, result['player_damage'] - defense)
                    player.health -= final_damage
                    print(f"You took {final_damage} damage!")
                return result['message']
                
        print(f"There is no {target} here to attack.")

class TalkCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("Who would you like to talk to?")
            return
            
        target = ' '.join(self.args)
        location = game_state.current_location
        
        for entity in location.entities:
            if target.lower() in entity.name.lower():
                return entity.talk(game_state)
                
        print(f"There is no one here called {target} to talk to.")

class FeedCommand(Command):
    def execute(self, game_state):
        if len(self.args) < 2:
            print("Usage: feed <creature> <item>")
            return
            
        target = self.args[0]
        item_name = ' '.join(self.args[1:])
        location = game_state.current_location
        
        # First find the entity
        target_entity = None
        for entity in location.entities:
            if target.lower() in entity.name.lower():
                target_entity = entity
                break
                
        if not target_entity:
            print(f"There is nothing here called {target} to feed.")
            return
            
        # Then find the item in inventory
        for item in game_state.player.inventory:
            if item_name.lower() in item.name.lower():
                result = target_entity.feed(item, game_state)
                # Check for story progression
                story_update = game_state.story.check_progress(game_state, "feed", 
                    {"target": target_entity.name, "item": item.name})
                if story_update:
                    print("\n" + "="*50)
                    print("New chapter unlocked!")
                    print(story_update)
                return result
                
        print(f"You don't have any {item_name} to feed them.") 

class JournalCommand(Command):
    def execute(self, game_state):
        game_state.player.show_journal() 

class RestCommand(Command):
    def execute(self, game_state):
        player = game_state.player
        if game_state.current_location.is_safe():
            player.fatigue = 0
            player.health = min(player.health + 20, player.max_health)
            print("You rest for a while. Health and energy restored!")
        else:
            print("It's not safe to rest here!") 

class StatusCommand(Command):
    def execute(self, game_state):
        player = game_state.player
        print("\n=== Status ===")
        print(f"Health: {player.health}/{player.max_health}")
        print(f"Hunger: {player.hunger}/100")
        print(f"Energy: {100 - player.fatigue}/100")
        print("\nEquipment:")
        for slot, item in player.equipped.items():
            print(f"{slot}: {item.name if item else 'None'}")
        damage, defense = player.get_stats()
        print(f"\nDamage: {damage}")
        print(f"Defense: {defense}") 

class EquipCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to equip?")
            return
            
        item_name = ' '.join(self.args)
        player = game_state.player
        
        for item in player.inventory:
            if item_name.lower() in item.name.lower():
                result = player.equip(item)
                print(result)
                return
                
        print(f"You don't have a {item_name} to equip.") 

class SaveCommand(Command):
    def execute(self, game_state):
        filename = "save.json"
        if self.args:
            filename = f"{' '.join(self.args)}.json"
        result = game_state.save_system.save_game(game_state, filename)
        print(result)

class LoadCommand(Command):
    def execute(self, game_state):
        filename = "save.json"
        if self.args:
            filename = f"{' '.join(self.args)}.json"
        result = game_state.save_system.load_game(game_state, filename)
        print(result) 

class TimeCommand(Command):
    def execute(self, game_state):
        print(f"\n{game_state.time.get_day()}")
        print(f"Time: {game_state.time.get_time_of_day()}")

class WaitCommand(Command):
    def execute(self, game_state):
        minutes = 10
        if self.args:
            try:
                minutes = int(self.args[0])
            except ValueError:
                print("Please specify minutes as a number.")
                return
        game_state.advance_time(minutes)
        print(f"You wait for {minutes} minutes...")

class ReliefCommand(Command):
    def execute(self, game_state):
        game_state.advance_time(5)
        game_state.player.bladder = 100
        print("You feel much better.")

class DrinkCommand(Command):
    def execute(self, game_state):
        if "water" in [item.name for item in game_state.player.inventory]:
            game_state.advance_time(2)
            game_state.player.thirst = min(100, game_state.player.thirst + 30)
            print("You take a drink of water.")
        else:
            print("You need water to drink!") 

class SurveyCommand(Command):
    def execute(self, game_state):
        location = game_state.current_location
        print("\n=== Surveying Your Surroundings ===")
        
        # Basic description
        print(location.description)
        
        # Check all directions
        for direction in ['north', 'east', 'south', 'west']:
            location.look_direction(direction)
            
        # Detailed environment check (chance to spot hidden things)
        details = location.get_detailed_survey(game_state)
        if details:
            print("\nUpon closer inspection:")
            for detail in details:
                print(f"- {detail}") 

class CampCommand(Command):
    def execute(self, game_state):
        location = game_state.current_location
        print("\n=== Setting up Camp ===")
        
        # Check if location is safe
        if any(entity.hostile for entity in location.entities):
            print("You can't set up camp here - there are hostile creatures nearby!")
            return
            
        print("You gather materials and set up a small camp.")
        print("\nAvailable actions:")
        print("1. Cook food")
        print("2. Rest")
        print("3. Cancel")
        
        choice = input("\nWhat would you like to do? ")
        
        if choice == "1":
            self._cook_food(game_state)
        elif choice == "2":
            self._rest(game_state)
            
    def _cook_food(self, game_state):
        print("\nCooking options:")
        print("1. Cook raw food")
        print("2. Prepare meal (combine foods)")
        print("3. Make tea from herbs")
        print("4. Cancel")
        
        choice = input("\nWhat would you like to do? ")
        
        if choice == "1":
            self._cook_raw_food(game_state)
        elif choice == "2":
            self._prepare_meal(game_state)
        elif choice == "3":
            self._make_tea(game_state)
            
    def _prepare_meal(self, game_state):
        food_items = [item for item in game_state.player.inventory 
                     if item.type == "food" and "raw" not in item.name.lower()]
        
        if len(food_items) < 2:
            print("You need at least 2 food items to prepare a meal.")
            return
            
        print("\nAvailable ingredients:")
        for i, item in enumerate(food_items, 1):
            print(f"{i}. {item.name}")
            
        try:
            print("\nSelect two ingredients (e.g., '1 2'):")
            choices = input().split()
            if len(choices) != 2:
                return
                
            idx1, idx2 = map(lambda x: int(x) - 1, choices)
            item1 = food_items[idx1]
            item2 = food_items[idx2]
            
            # Create a better meal
            meal_value = (item1.food_value + item2.food_value) * 1.2
            meal = Item(f"prepared meal", 
                       f"A tasty meal made from {item1.name} and {item2.name}",
                       "food", food_value=meal_value)
                       
            game_state.player.remove_item(item1)
            game_state.player.remove_item(item2)
            game_state.player.add_item(meal)
            game_state.advance_time(20)
            print(f"\nYou prepare a delicious meal combining {item1.name} and {item2.name}!")
            
        except (ValueError, IndexError):
            print("Invalid choice.")
            
    def _make_tea(self, game_state):
        herbs = [item for item in game_state.player.inventory 
                if item.type == "food" and "herb" in item.name.lower()]
        
        if not herbs:
            print("You need herbs to make tea.")
            return
            
        print("\nAvailable herbs:")
        for i, item in enumerate(herbs, 1):
            print(f"{i}. {item.name}")
            
        try:
            choice = int(input("\nWhich herbs to use? ")) - 1
            if choice < 0 or choice >= len(herbs):
                return
                
            herb = herbs[choice]
            tea = Item("herbal tea", 
                      f"A soothing tea made from {herb.name}",
                      "food", food_value=herb.food_value * 1.5)
                      
            game_state.player.remove_item(herb)
            game_state.player.add_item(tea)
            game_state.advance_time(10)
            print(f"\nYou prepare a refreshing tea from {herb.name}!")
            
        except (ValueError, IndexError):
            print("Invalid choice.")
            
    def _rest(self, game_state):
        game_state.advance_time(60)  # Rest for an hour
        game_state.player.energy = min(100, game_state.player.energy + 30)
        print("You rest by the campfire. Energy restored.") 

class EatCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to eat?")
            return
            
        item_name = ' '.join(self.args)
        player = game_state.player
        
        for item in player.inventory:
            if item_name.lower() in item.name.lower():
                result = player.consume_food(item)
                print(result)
                return
                
        print(f"You don't have any {item_name} to eat.") 

class UnequipCommand(Command):
    def execute(self, game_state):
        if not self.args:
            print("What would you like to unequip?")
            return
            
        slot = ' '.join(self.args).lower()
        player = game_state.player
        
        # Allow both slot names and item names
        if slot in player.equipped:
            if player.equipped[slot]:
                item = player.equipped[slot]
                player.unequip(slot)
                print(f"Unequipped {item.name}")
            else:
                print(f"Nothing equipped in {slot} slot")
        else:
            # Try to find by item name
            for slot, item in player.equipped.items():
                if item and slot.lower() in item.name.lower():
                    player.unequip(slot)
                    print(f"Unequipped {item.name}")
                    return
            print(f"No equipped item matches '{slot}'")

class EquipmentCommand(Command):
    def execute(self, game_state):
        player = game_state.player
        print("\n=== Equipment ===")
        
        total_damage, total_defense = player.get_stats()
        print(f"Total Damage: {total_damage}")
        print(f"Total Defense: {total_defense}")
        
        print("\nEquipped Items:")
        for slot, item in player.equipped.items():
            if item:
                stats = []
                if item.damage_bonus:
                    stats.append(f"+{item.damage_bonus} damage")
                if item.defense_bonus:
                    stats.append(f"+{item.defense_bonus} defense")
                stat_text = f" ({', '.join(stats)})" if stats else ""
                print(f"{slot.capitalize()}: {item.name}{stat_text}")
            else:
                print(f"{slot.capitalize()}: Nothing equipped") 

class CraftCommand(Command):
    def execute(self, game_state):
        recipes = {
            "torch": {"wood": 1, "cloth": 1},
            "bandage": {"herbs": 2},
            "water_flask": {"water": 1, "leather": 1}
        }
        # Show available recipes based on inventory 

class QuestCommand(Command):
    def execute(self, game_state):
        print("\n=== Active Quests ===")
        for quest_id, quest in game_state.story.quests.items():
            if not quest["completed"]:
                print(f"\n{quest['name']}:")
                current_stage = 1
                for stage_num, desc in quest["stages"].items():
                    status = "✓" if stage_num < current_stage else "•"
                    print(f"{status} {desc}") 

class AchievementsCommand(Command):
    def execute(self, game_state):
        print("\n=== Achievements ===")
        for ach_id, ach in game_state.achievements.achievements.items():
            status = "✓" if ach["unlocked"] else "□"
            if "progress" in ach and not ach["unlocked"]:
                if isinstance(ach["progress"], set):
                    progress = f" ({len(ach['progress'])}/{ach['target']})"
                else:
                    progress = f" ({ach['progress']}/{ach['target']})"
            else:
                progress = ""
            print(f"{status} {ach['name']}{progress}: {ach['description']}") 

class StatsCommand(Command):
    def execute(self, game_state):
        player = game_state.player
        display = game_state.display
        
        # Get player stats
        stats = {
            'health': player.health,
            'max_health': player.max_health,
            'energy': player.energy,
            'level': player.level,
            'exp': player.exp,
            'gold': player.gold,
            'attributes': {
                'Strength': player.strength,
                'Dexterity': player.dexterity,
                'Intelligence': player.intelligence,
                'Vitality': player.vitality,
                'Charisma': player.charisma,
                'Wisdom': player.wisdom,
                'Luck': player.luck
            },
            'skills': {
                'Melee Combat': player.skills.get('melee', 1),
                'Defense': player.skills.get('defense', 1),
                'Survival': player.skills.get('survival', 1),
                'Crafting': player.skills.get('crafting', 1)
            }
        }
        
        display.show_character_sheet(stats) 