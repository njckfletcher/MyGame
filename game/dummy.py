'''
Created on Dec 31, 2016

@author: root
'''

import os
import game_defs

dir_path = os.path.dirname(os.path.realpath(__file__))

cwd = os.getcwd()

running = True

while running:
    
    game_defs.intro()
    
    game_defs.load_option()