'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import os
import random
import pickle
import time
from game import game_defs, text_parse
from game.game_defs import print_by_char, print_dots

# System objects
if os.name == 'posix':
    SAVES_DIR = os.getcwd() + "/saves/"
else:
    SAVES_DIR = os.getcwd() + "\\saves\\"

RUNNING = True
CMD_IN_PROGRESS = True
SYS_PROMPTS = ["What do you want to do?: ",
               "What now?: ",
               "What would you like to do next?: ",
               "Enter your command(s): "]
JUST_SAVED = False

game_defs.intro()

with open(SAVES_DIR + game_defs.load_option(SAVES_DIR) + '.dat', 'rb') as f:
    HERO, MAP_OBJECTS = pickle.load(f)

# Game start
while RUNNING:
    print('--------------------------------------------')
    time.sleep(0.5)
    game_defs.display_level(HERO.get_level())
    time.sleep(0.5)
    print('\n--------------------------------------------')
    game_defs.display_prompt(MAP_OBJECTS[HERO.get_location()], HERO)

    while CMD_IN_PROGRESS:
        print('--------------------------------------------')
        ARG = text_parse.parse_command(SYS_PROMPTS[random.randrange(len(SYS_PROMPTS))],
                                       HERO,
                                       MAP_OBJECTS,
                                       SAVES_DIR,
                                       JUST_SAVED)

        if ARG == 'quit':
            CMD_IN_PROGRESS = False
        elif ARG == 'saved':
            JUST_SAVED = True
        elif ARG == 'not saved':
            JUST_SAVED = False

        if HERO.get_health() <= 0:
            print('')
            print_by_char('You died..  Game over.', 0.005)
            print('')
            game_defs.remove_char(HERO.get_name(), SAVES_DIR)
            CMD_IN_PROGRESS = False

    print_by_char('Quitting 7 Stories', 0.005, False)
    print_dots(2)
    print('\n--------------------------------------------')
    break
