'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import game_defs, game_objects, text_parse
import os
import random
import pickle
from game_defs import print_by_char

# System objects
if os.name == 'posix':
    saves_dir = os.getcwd() + "/saves/"
else:
    saves_dir = os.getcwd() + "\saves\\"

running = True
command_in_progress = True
system_prompts = ["What do you want to do?: ", 
                  "What now?: ", 
                  "What would you like to do next?: ", 
                  "Enter your command(s): "]

game_defs.intro()
        
with open(saves_dir + game_defs.load_option(saves_dir) + '.dat', 'rb') as f:
    hero, map_objects, item_objects = pickle.load(f)
        
# Game start
while running:            
    while command_in_progress:
        print('------------------------------------------')
        arg = text_parse.parse_command(system_prompts[random.randrange(len(system_prompts))], 
                                 hero, 
                                 hero.location,  
                                 map_objects,
                                 item_objects,
                                 saves_dir)
        
        if arg == 'quit':
            print_by_char('Quitting..', 0.01)
            command_in_progress = False
    
    
    
    while not command_in_progress:
        print('------------------------------------------')
        
        print_by_char('Would you like to save before quitting (y\\n): ', 0.01, False)
        decision = input().lower()
        
        if decision == "y" or decision == "yes":
            print('------------------------------------------')
            game_defs.save_game(hero, map_objects, item_objects, saves_dir)
            break
        elif decision == "n" or decision == "no":
            break
        else:
            print('------------------------------------------')
            print_by_char('Invalid command!', 0.01)
            
    break