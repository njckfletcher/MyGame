'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
from game_defs import print_by_char

class Player:
    health = 100
    location = 'lobby'
    level = 1
    journey = 1
    
    weight = 0
    
    def __init__(self, name):
        self.name = name
        self.inventory = ['laptop']
        
        
    def display_health(self):
        print_by_char('Health: ' + str(self.health) + '%', 0.01)
        
        
    def display_location(self):
        print_by_char('Location: ' + self.location[0:1].upper() + self.location[1:len(self.location)], 0.01)
        
        
    def set_location(self, location):
        if self.location == location:
            print_by_char('>>> ' + str(self.name) + ' is already at the ' + str(location), 0.01)
        else:
            self.location = location
            print_by_char('>>> ' + str(self.name) + ' moved to the ' + location[0:1].upper() + location[1:len(location)], 0.01)
            
            
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
    
    
class Lab(Environment):
    name = 'lab'
    
    def __init__(self):
        self.inventory = ['phone']
    
    
class Dorm(Environment):
    name = 'dorm'
    pass


class Room(Environment):
    name = 'room'
    pass


class Club(Environment):
    name = 'club'
    pass


class FB_lobby(Environment):
    
    # Prompts:
    name = ["Location: Lobby"]
    opener = ['Welcome to Facebook, the home of all',
              'things social.  Our web server is the',
              'heart of our service, providing users with',
              'the capability of communicating with their',
              'friends and loved ones over the Internet.',
              'With top of the line security, users can',
              'safely use our service without the worry.\n']
    base = ['The lobby is a small room with a',
            'receptionist\'s desk and a door across from',
            'it.  The front desk has a computer on it',
            'labeled \'lobby_computer\'.']
    
    def __init__(self):
        self.first_visit = True
        self.current_prompt = [self.name, self.opener, self.base]
        
    
    def new_prompt(self, first_visit, current_prompt):
        if first_visit:
            current_prompt.pop(1)
            self.first_visit = False
    
    

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