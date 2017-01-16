'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
from game_defs import print_by_char, display_prompt, print_dots
import random
import attacks

class Player:
    
    
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.location = 'Front Lobby'
        self.level = 1
        self.journey = 1
        self.visited = ['Front Lobby']    
        self.weight = 0
        self.inventory = ['laptop']
        
        
    def receive_damage(self, damage):
        self.health -= damage
        
    
    def get_visited(self):
        return self.visited
        
    
    def display_level(self):
        print_by_char('Level: {}'.format(self.level), 0.005)
        
    
    def get_level(self):
        return self.level
    
    
    def display_journey(self):
        print_by_char('Journey: {}'.format(self.journey), 0.005)
        
        
    def get_journey(self):
        return self.journey
        
        
    def display_health(self):
        print_by_char('Health: {}%'.format(self.health), 0.005)
        
        
    def display_location(self):
        print_by_char('Location: {}'.format(self.location), 0.005)
        
        
    def set_location(self, location, player, phrase):
        
        if self.location == location.get_name():
            print_by_char('>>> {} is already at the {}.'.format(self.name, self.location), 0.005)
            
        else:
            self.location = location.get_name()
            if location.get_name() in self.visited:
                print_by_char('>>> {} moved to the {}.'.format(self.name, self.location), 0.005)
            else:
                print_by_char('>>> {} moved to the {}.'.format(self.name, phrase), 0.005)
            if location.first_visit:
                self.visited.append(location.get_name())
                print('          ----------------------')
                display_prompt(location, player)
                
            
    def get_location(self):
        return self.location
    
    
    def display_weight(self):
        print_by_char('Weight: {}'.format(self.weight), 0.005)
        
        
    def set_name(self, name):
        self.name = name
    
    
    def display_name(self):
        print_by_char('Name: {}'.format(self.name), 0.005)
        
    
    def get_name(self):
        return self.name
        
        
    def display_inventory(self):
        print_by_char('Inventory: {}'.format(self.inventory), 0.005)
        
    
    def get_inventory(self):
        return self.inventory
        
        
    def add_item(self, item, action):
        self.inventory.append(item)
        if action == 'take':
            print_by_char('>>> {} took the {}.'.format(self.name, item), 0.005)
        elif action == 'pick' or action == 'pickup':
            print_by_char('>>> {} picked up the {}.'.format(self.name, item), 0.005)
        else:
            print_by_char('>>> {} grabbed the {}.'.format(self.name, item), 0.005)
        
        
        
    def display_stats(self):
        print_by_char('Name: {} | Journey: {} | Level: {}'.format(self.name, self.journey, self.level), 0.005)
        self.display_health()
        self.display_location()
        self.display_inventory()
        self.display_weight()
        
        
class Environment:
    name = None
    inventory = []
    
    
    def add_item(self, item):
        self.inventory.append(item)
        
        
    def remove_item(self, item):
        self.inventory.remove(item)
        
        
    def get_inventory(self):
        return self.inventory
    
    
    def get_name(self):
        return self.name


class Front_lobby(Environment):
    
    # Local location names
    front_lobby = {'front lobby': 'Front Lobby', 'lobby': 'Front Lobby'}
    south_hall = {'south hall': 'South Hall', 'hall': 'South Hall'}
    
    # Check if player has been to local locations
    visited_south_hall = False
    
    # Prompts:
    location = ["Location: Front Lobby"]
             #'--------------------------------------------'
    opener = ['You enter the doors of the Internet.  You',
              'walk into a bright room with a reception',
              'desk to the right and a door to the left.',
              'The desk has a computer on it labeled',
              '"Reception Computer".  Above you is a sign',
              'hanging from the ceiling that says',
              '"Front Lobby".  A plaque sits next to the',
              'door reading:',
              '',
              '"Welcome to Facebook, the home of all',
              'things social.  Our web server is the',
              'heart of our service, providing users with',
              'the capability of communicating with their',
              'friends and loved ones over the Internet.',
              'With top of the line security, users can',
              'safely use our service without the worry."']
    
    base_01 = ['There is a door and a reception desk.  The',
               'desk has a computer on it labeled',
               '"Lobby Computer".']
              #'--------------------------------------------'
    base_02 = ['There is a reception desk with a computer',
               'on it.  The computer is labeled "Reception',
               'Computer".  A doorway leads to a hall.']
    base_03 = ['There is a reception desk with a computer',
               'on it.  The computer is labeled "Reception',
               'Computer".  A doorway leads to the',
               'South Hall.']
    
    
    def __init__(self):
        self.name = 'Front Lobby'
        self.first_visit = True
        self.current_prompt = [self.opener]
        self.south_hall_door = Door('south hall door', False, True)
        self.doors = {'door': self.south_hall_door, 'left door': self.south_hall_door}
        self.avail_locs = [self.front_lobby]
        self.inventory = ['phone', 'wooden silver laptop']
        
    
    def open_door(self, phrase, player):
        Door.open_door(self.doors[phrase], phrase)
        self.update_current_prompt(self.first_visit, self.current_prompt, player)
        
    
    def update_current_prompt(self, first_visit, current_prompt, player):
        self.update_avail_locs()
        
        if first_visit:
            current_prompt.pop(0)
            self.current_prompt.append(self.location)
            self.current_prompt.append(self.base_01)
            self.first_visit = False
        
        if self.base_02 not in self.current_prompt:
            for loc in self.avail_locs:
                for name in loc:
                    if loc[name] == 'South Hall':
                        self.current_prompt.pop(1)
                        self.current_prompt.append(self.base_02)
        
        if self.base_03 not in self.current_prompt:
            if 'South Hall' in  player.get_visited():
                self.current_prompt.pop(1)
                self.current_prompt.append(self.base_03)
                
        
        return self.current_prompt
            
    
    def update_avail_locs(self):
        
        if 'south_hall' not in self.avail_locs:
            if self.south_hall_door.open == True:
                self.avail_locs.append(self.south_hall)
                
    
    
class South_Hall(Environment):
    
    # Local location names
    south_hall = {'south hall': 'South Hall', 'hall': 'South Hall'}
    front_lobby = {'front lobby': 'Front Lobby', 'lobby': 'Front Lobby'}
    
     # Prompts:
    location = ["Location: South Hall"]
             #'--------------------------------------------'
    opener = ["             -The South Hall-             ",
              "",
              "You step into the hall.  The south hall is",
              "a short and narrow hallway with a door at",
              "the far end.  A doorway leading back to",
              "the front lobby remains behind you.  To",
              "your right, 3 lockers sit mounted on the",
              "wall, each with a label as follows:",
              "     - Forbidden Locker",
              "     - Gentleman's Locker",
              "     - Desperation Locker"]
    
    base_01 = ['This is the base_01 for the South Hall']
    
    
    def __init__(self):
        self.name = 'South Hall'
        self.first_visit = True
        self.current_prompt = [self.opener]
        self.doors = {}
        self.avail_locs = [self.south_hall, self.front_lobby]
        
    
    def update_current_prompt(self, first_visit, current_prompt, player):
        if first_visit:
            current_prompt.pop(0)
            self.current_prompt.append(self.location)
            self.current_prompt.append(self.base_01)
            self.first_visit = False
        
        return self.current_prompt
    
    
    def update_avail_locs(self):
        #avail_locs = [self.south_hall, self.front_lobby]
        pass
        #return avail_locs


class Door(object):
    
    name = None
    
    south_hall_door_opener = 'The doorway leads to a hall.'
    
    def __init__(self, name, open, unlocked):
        self.name = name
        self.open = open
        self.unlocked = unlocked
        
        
    def get_name(self):
        return self.name
        
        
    def open_door(self, phrase):
        if not self.open:
            if self.unlocked:
                self.open = True
                print_by_char('>>> Opened the {}.'.format(phrase), 0.005)
                print('          ----------------------')
                if self.get_name() == 'south hall door':
                    print(self.south_hall_door_opener)
                
            else:
                print_by_char('>>> The {} is locked.'.format(phrase), 0.005)
        else:
            print_by_char('>>> The {} is already open.'.format(phrase), 0.005)
            
            
class Item():
    weight = 1
    
    
class Phone(Item):
    
    def use(self):
        active = True
        password = 'P@ssword'
        
        while active:
            decision = input('Enter your passcode: ')
            
            if decision == password:
                print('You unlocked the phone!')
                print('Now leaving the phone..')
                active = False
            elif decision == 'exit':
                active = False
            else:
                print('You entered the wrong password')
            #active = False

class Laptop(Item): 
    
    def __init__(self):
            self.accounts = {}
            self.power_state = False
            self.default_acc = None
            self.current_acc = None
            self.logged_in = False
        
    def use(self):
        
        print_by_char('"Booting', 0.005, False), print_dots(2, True)
        self.power_state = True
        
        while self.power_state:
            
            if not self.accounts:
                print_by_char('You must create an account before you can', 0.005)
                print_by_char('use the computer.', 0.005)
                print('')
                self.current_acc = self.create_account()
                print('')
            
            if self.default_acc:
                self.current_acc = self.default_acc
                
            while not self.logged_in:
                if self.current_acc:
                    print_by_char('Welcome, {}.'.format(self.current_acc), 0.005)
                    print_by_char('>> 1: Login', 0.005)
                    print_by_char('>> 2: Switch accounts', 0.005)
                    print_by_char('>> 3: Shutdown', 0.005)
                    print_by_char('>> 4: Create new account', 0.005)
                    
                    while True:
                        print('')
                        print_by_char('Enter number : ', 0.005, False)
                        option = input()
                        print('')
                        if option == '1':
                            self.logged_in = self.accounts[self.current_acc].login()
                            break
                        elif option == '2':
                            self.current_acc = self.switch_acc()
                            break
                        elif option == '3':
                            return self.shut_down()
                        elif option == '4':
                            self.current_acc = self.create_account()
                            break
                        else:
                            print_by_char('Please enter a number.', 0.005)
                else:
                    self.current_acc = self.switch_acc()
            
            while self.logged_in:
                self.logout()
            
            return self.shut_down()
                    
            
        
    
    def create_account(self):
        name_set = False
        password_set = False
        
        while name_set is False:
            name_taken = False
            print_by_char('Create a username: ', 0.005, False)
            name = input()
            
            for account in self.accounts:
                if name == account:
                    name_taken = True
                    print('')
                    print_by_char("> This name is already taken.", 0.005)
                    print('')
                    break
            
            if len(name) < 20 and not name_taken:
                name_set = True
            elif len(name) > 20:
                print('')
                print_by_char('> Max amount of characters: 20', 0.005)
                print_by_char('> Try again..', 0.005)
                print('')
        
        while password_set is False:
            print_by_char('Create a password: ', 0.005, False)
            password = input()
            pass_chars = []
            for char in password: pass_chars.append(char)
            
            if password == 'quit':
                print('')
                print_by_char('> You cannot use that as a password!', 0.005)
                print('')
                continue
            elif ' ' in pass_chars:
                print('')
                print_by_char('> You cannot include a space!', 0.005)
                print('')
                continue
            
            print_by_char('Re-enter password: ', 0.005, False)
            retype = input()
            
            if password == retype:
                password_set = True
            else:
                print('')
                print_by_char('> Passwords do not match!', 0.005)
                print('')
            
        print_by_char('Password hint: ', 0.005, False)
        pass_hint = input()
        
        print("")
        self.accounts[name] = self.Account(name, password, pass_hint)
        print_dots(3)
        print_by_char(' Account created successfully.', 0.005)
        print('')
        while True:
            print_by_char('Set as default? (y\\n): ', 0.005, False)
            option = input().lower()
            print('')
            if option == "y" or option == "yes":
                self.default_acc = name
                break
            elif option == "n" or option == "no":
                break
            else:
                print_by_char('> Please answer yes or no.', 0.005)
                print('')
        
        return name
        
    
    def switch_acc(self):
        print_by_char('Please select an account:', 0.005)
        
        acc_dict = {}
        
        counter = 1
        for account in self.accounts:
            acc_dict[str(counter)] = account
            print_by_char('>> {}: {}'.format(counter, account), 0.005)
            counter += 1
        
        while True:
            print('')
            print_by_char('Enter number : ', 0.005, False)
            option = input().lower()
            print('')
            
            if option in acc_dict:
                return acc_dict[option]
            else:
                print_by_char('> You must enter a number.', 0.005)
    
    
    def logout(self):
        print('')
        print_by_char('Logging out..', 0.005)
        self.logged_in = False
        print('')
    
    
    class Account():
        
        def __init__(self, un, pw, ph):
            self.password = pw
            self.username = un
            self.pass_hint = ph
            
        def get_username(self):
            return self.username
        
        def login(self):
            while True:
                print_by_char('Please enter your password: ', 0.005, False)
                response = input()
                
                if response == self.password:
                    print('')
                    print_by_char('> Computer unlocked.', 0.005)
                    return True
                elif response == 'quit':
                    print('')
                    print_by_char('> Quitting.."', 0.005)
                    return False
                else:
                    print('')
                    print_by_char('> Wrong password!', 0.005)
                    self.display_pass_hint()
                    print('')
                    
        
        def display_pass_hint(self):
            print_by_char('> Password hint: ' + self.pass_hint, 0.005)
            
            
    def shut_down(self):
        print_by_char('Shutting down', 0.005, False), print_dots(2), print('"')
        self.power_state = False
        
        
        
class Enemy():
    
    reward = 1
    
    def receive_damage(self, damage):
        self.health -= damage


class Anon(Enemy):

    def attack(self, player):
        attacks.push(player)
    