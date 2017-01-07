'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
from game_defs import print_by_char
import random
import attacks

class Player:
    health = 100
    location = 'lobby'
    level = 1
    journey = 1
    
    weight = 0
    
    def __init__(self, name):
        self.name = name
        self.inventory = ['laptop']
        
        
    def receive_damage(self, damage):
        self.health -= damage
        
        
    def display_health(self):
        print_by_char('Health: ' + str(self.health) + '%', 0.01)
        
        
    def display_location(self):
        loc_words = [word for word in self.location.split()]
        
        print_by_char('Location: ', 0.01, False)
        for word in loc_words:
            print_by_char(word[0:1].upper() + word[1:len(word)], 0.01, False)
            print_by_char(' ', 0.01, False)
        print('')
        
        
    def set_location(self, location):
        loc_words = [word for word in location.split()]
        
        if self.location == location:
            print_by_char('>>> ' + str(self.name) + ' is already at the ', 0.01, False)
            for word in loc_words:
                print_by_char(word[0:1].upper() + word[1:len(word)], 0.01, False)
                if loc_words.index(word) < len(loc_words) - 1:
                     print_by_char(' ', 0.01, False)
            print('.')
        else:
            self.location = location
            print_by_char('>>> ' + str(self.name) + ' moved to the ', 0.01, False)
            for word in loc_words:
                print_by_char(word[0:1].upper() + word[1:len(word)], 0.01, False)
                if loc_words.index(word) < len(loc_words) - 1:
                    print_by_char(' ', 0.01, False)
            print('.')
            
            
    def get_location(self):
        return self.location
    
    
    def display_weight(self):
        print_by_char('Weight: ' + str(self.weight), 0.01)
        
        
    def set_name(self, name):
        self.name = name
    
    
    def display_name(self):
        print_by_char('Name: ' + str(self.name), 0.01)
        
    
    def get_name(self):
        return self.name
        
        
    def display_inventory(self):
        print_by_char('Inventory: ' + str(self.inventory), 0.01)
        
    
    def get_inventory(self):
        return self.inventory
        
        
    def add_item(self, item, action):
        self.inventory.append(item)
        if action == 'take':
            print_by_char('>>> ' + str(self.name) + ' took the ' + str(item), 0.01)
        elif action == 'pick' or action == 'pickup':
            print_by_char('>>> ' + str(self.name) + ' picked up the ' + str(item), 0.01)
        else:
            print_by_char('>>> ' + str(self.name) + ' grabbed the ' + str(item), 0.01)
        
        
        
    def display_stats(self):
        self.display_name()
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


class FB_lobby(Environment):
    
    # Local location names
    lobby = {'front lobby': 'lobby', 'lobby': 'lobby'}
    south_hall = {'south hall': 'south hall', 'hall': 'south hall'}
    
    # Prompts:
    name = ["Location: Lobby"]
    opener = ['Welcome to Facebook, the home of all',
              'things social.  Our web server is the',
              'heart of our service, providing users with',
              'the capability of communicating with their',
              'friends and loved ones over the Internet.',
              'With top of the line security, users can',
              'safely use our service without the worry.']
    base = ['The lobby is a small room with a',
            'receptionist\'s desk and a door across from',
            'it.  The front desk has a computer on it',
            'labeled \'lobby computer\'.']
    
    def __init__(self):
        self.first_visit = True
        self.current_prompt = [self.name, self.opener, self.base]
        self.south_hall_door = Door(False, True, self.south_hall)
        self.doors = {'door': self.south_hall_door}
        
    
    def open_door(self, door):
        Door.open_door(self.doors[door])
        
    
    def new_prompt(self, first_visit, current_prompt):
        if first_visit:
            current_prompt.pop(1)
            self.first_visit = False
            
    
    def get_avail_locs(self):
        avail_locs = [self.lobby]
        
        if 'south_hall' not in avail_locs:
            if self.south_hall_door.open == True:
                avail_locs.append(self.south_hall)
        
        return avail_locs
                
    
    
class South_Hall():
    
    # Local location names
    south_hall = {'south hall': 'south hall', 'hall': 'south hall'}
    lobby = {'front lobby': 'lobby', 'lobby': 'lobby'}
    
     # Prompts:
    name = ["Location: South Hall"]
    opener = ['This is the opener to the South Hall.']
    
    
    def __init__(self):
        self.first_visit = True
        self.current_prompt = [self.name, self.opener]
        self.doors = {}
        
    
    def new_prompt(self, first_visit, current_prompt):
        if first_visit:
            current_prompt.pop(1)
            self.first_visit = False
    
    
    def get_avail_locs(self):
        avail_locs = [self.south_hall, self.lobby]
        
        return avail_locs


class Door(object):
    
    def __init__(self, open, unlocked, loc_dict):
        self.open = open
        self.unlocked = unlocked
        self.loc_dict = loc_dict
        
        
    def open_door(self):
        if not self.open:
            if self.unlocked:
                self.open = True
                print_by_char('>>> Opened the door.', 0.01)
                return self.loc_dict
            else:
                print_by_char('>>> The door is locked.', 0.01)
        else:
            print_by_char('>>> The door is already open.', 0.01)
            return
        
    

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
    