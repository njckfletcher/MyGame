'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import game_defs, game_objects, text_parse
import os
import random
import pickle
from game_defs import print_by_char, print_dots
import time

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
just_saved = False

#game_defs.intro()
        
with open(saves_dir + game_defs.load_option(saves_dir) + '.dat', 'rb') as f:
    hero, map_objects = pickle.load(f)
        
# Game start
while running:
    print('--------------------------------------------')
    time.sleep(0.5)
    game_defs.display_level(hero.get_level())
    time.sleep(0.5)
    print('\n--------------------------------------------')
    game_defs.display_prompt(map_objects[hero.get_location()], hero)
                    
    while command_in_progress:
        print('--------------------------------------------')
        arg = text_parse.parse_command(system_prompts[random.randrange(len(system_prompts))], 
                                 hero,  
                                 map_objects,
                                 saves_dir,
                                 just_saved)
        hero.just_saved = False
        
        if arg == 'quit':
            command_in_progress = False
        elif arg == 'saved':
            just_saved = True
        elif arg == 'not saved':
            just_saved = False
        
        if hero.get_health() <= 0:
            print('')
            print_by_char('You died..  Game over.', 0.005)
            print('')
            game_defs.remove_char(hero.get_name(), saves_dir)
            command_in_progress = False
    
    print_by_char('Quitting 7 Stories', 0.005, False)
    print_dots(2)
    print('\n--------------------------------------------') 
    break