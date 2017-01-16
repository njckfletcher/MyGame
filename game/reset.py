'''
Created on Jan 7, 2017

@author: root
'''
from game import game_defs
import os

if os.name == 'posix':
    saves_dir = os.getcwd() + "/saves/"
else:
    saves_dir = os.getcwd() + "\saves\\"
    
os.remove(saves_dir + 'Hunter' + '.dat')
game_defs.init_char('Hunter', saves_dir)

print('Character reset.')