'''
Created on Dec 31, 2016

@author: Hunter Malm
'''
from game import game_objects

envi = game_objects.South_Hall()

containers = envi.containers
for container in containers:
    
    inventory = containers[container].get_inventory()
    for item in inventory:
        
        print(item)