'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
from game_defs import print_by_char
from game_defs import display_prompt
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
        print_by_char('Level: {}'.format(self.level), 0.01)
        
    
    def get_level(self):
        return self.level
    
    
    def display_journey(self):
        print_by_char('Journey: {}'.format(self.journey), 0.01)
        
        
    def get_journey(self):
        return self.journey
        
        
    def display_health(self):
        print_by_char('Health: {}%'.format(self.health), 0.01)
        
        
    def display_location(self):
        print_by_char('Location: {}'.format(self.location), 0.01)
        
        
    def set_location(self, location, player):
        
        if self.location == location.get_name():
            print_by_char('>>> {} is already at the {}.'.format(self.name, self.location), 0.01)
            
        else:
            self.location = location.get_name()
            print_by_char('>>> {} moved to the {}.'.format(self.name, self.location), 0.01)
            if location.first_visit:
                self.visited.append(location.get_name())
                print('           --------------------')
                display_prompt(location, player)
                
            
    def get_location(self):
        return self.location
    
    
    def display_weight(self):
        print_by_char('Weight: {}'.format(self.weight), 0.01)
        
        
    def set_name(self, name):
        self.name = name
    
    
    def display_name(self):
        print_by_char('Name: {}'.format(self.name), 0.01)
        
    
    def get_name(self):
        return self.name
        
        
    def display_inventory(self):
        print_by_char('Inventory: {}'.format(self.inventory), 0.01)
        
    
    def get_inventory(self):
        return self.inventory
        
        
    def add_item(self, item, action):
        self.inventory.append(item)
        if action == 'take':
            print_by_char('>>> {} took the {}.'.format(self.name, item), 0.01)
        elif action == 'pick' or action == 'pickup':
            print_by_char('>>> {} picked up the {}.'.format(self.name, item), 0.01)
        else:
            print_by_char('>>> {} grabbed the {}.'.format(self.name, item), 0.01)
        
        
        
    def display_stats(self):
        print_by_char('Name: {} | Journey: {} | Level: {}'.format(self.name, self.journey, self.level), 0.01)
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
             #'------------------------------------------'
    opener = ['You enter the doors of the Internet.  You',
              'walk into a bright room with a reception',
              'desk to the right and a door to the left.',
              'The desk has a computer on it labeled',
              '"Reception Computer".  Above you is a sign',
              'hanging from the cieling that says',
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
              #'------------------------------------------'
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
             #'------------------------------------------'
    opener = ['This is the opener to the South Hall.',
              'And this is another line!']
    
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
                print_by_char('>>> Opened the {}.'.format(phrase), 0.01)
                print('           --------------------')
                if self.get_name() == 'south hall door':
                    print(self.south_hall_door_opener)
                
            else:
                print_by_char('>>> The {} is locked.'.format(phrase), 0.01)
        else:
            print_by_char('>>> The {} is already open.'.format(phrase), 0.01)
            
            
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
    
    username = None
    password = None
    pass_hint = None
    
    def __init__(self, un, pw, ph):
        self.password = pw
        self.username = un
        self.pass_hint = ph
    
        
    def use(self):
        
        active = True
        while active:
            print_by_char('"Welcome ' + self.username, 0.01)
            print('')
            
            locked = True
            while locked:
                print_by_char('Please enter your password: ', 0.01, False)
                response = input()
                
                if response == self.password:
                    locked = False
                    print('')
                    print_by_char('> Computer unlocked.', 0.01)
                    print('')
                elif response == 'quit':
                    print('')
                    print_by_char('> Quitting.."', 0.01)
                    break
                else:
                    print('')
                    print_by_char('> Wrong password!', 0.01)
                    self.display_pass_hint()
                    print('')
            
            while not locked:
                print_by_char('Well, there\'s nothing to do here.  Leaving..."', 0.01)
                active = False
                break
            
            active = False
                
                
    def display_pass_hint(self):
        print_by_char('> Password hint: ' + self.pass_hint, 0.01)
        
        
class Enemy():
    
    reward = 1
    
    def receive_damage(self, damage):
        self.health -= damage


class Anon(Enemy):

    def attack(self, player):
        attacks.push(player)
    