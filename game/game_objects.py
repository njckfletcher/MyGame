'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
from game_defs import print_by_char

class Player:
    health = 100
    location = 'lab'
    
    weight = 0
    
    def __init__(self, name):
        self.name = name
        self.inventory = ['laptop']
        
        
    def display_health(self):
        print_by_char('Health: ' + str(self.health) + '%', 0.01)
        
        
    def display_location(self):
        print_by_char('Location: ' + str(self.location), 0.01)
        
        
    def set_location(self, location):
        if self.location == location:
            print_by_char('>>> ' + str(self.name) + ' is already at the ' + str(location), 0.01)
        else:
            self.location = location
            print_by_char('>>> ' + str(self.name) + ' moved to the ' + str(location), 0.01)
            
            
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
            print_by_char('Welcome ' + self.username, 0.01)
            
            locked = True
            while locked:
                print_by_char('Please enter your password: ', 0.01, False)
                response = input()
                
                if response == self.password:
                    locked = False
                    print('')
                    print_by_char('Computer unlocked.')
                    print('')
                else:
                    print('')
                    
                
            inp = input('Please enter your password: ')
            
            if inp == self.password:
                print('You unlocked the computer!')
                print('Now quitting.. ')
                active = False
            else:
                print('Wrong password!')