'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import game_objects, text_parse, game_defs
import random
import pickle

# System objects
running = True
system_prompts = ["What do you want to do?: ", 
                  "What now?: ", 
                  "What would you like to do next?: ", 
                  "Enter your command(s): "]
command_in_progress = True


# Game start
while running:

    game_defs.intro()
    
    decision = input('Would you like to load a save?').lower()
    
    if decision == 'y' or decision == 'yes' or decision == 'yea':
        loadin('savefile.dat')
    
    # Retrieving player name
    name_set = False
    while name_set is False:
        print('------------------------------------------')
        name = input('Enter your name: ')
        
        if len(name) > 20:
            print('------------------------------------------')
            print('Max amount of characters: 20')
            print('Try again..')
        else:
            name_set = True
            
    # Creating main player
    hero = game_objects.Player(name)
    
    map_objects = {'lab': game_objects.Lab(), 'dorm': game_objects.Dorm(), 'room': game_objects.Room(), 'club': game_objects.Club()}
    
    item_objects = {'phone' : game_objects.Phone()}
    
    #print('loading old save..')
    #with open('savefile.dat', 'rb') as f:
    #    hero, map_objects, item_objects = pickle.load(f)
    
    while command_in_progress:
        print('------------------------------------------')
        text_parse.parse_command(system_prompts[random.randrange(len(system_prompts))], 
                                 hero, 
                                 hero.location,  
                                 map_objects,
                                 item_objects)

    
def loadin(file):
    with open(file, 'rb') as f:
        hero, map_objects, item_objects = pickle.load(f) 
    