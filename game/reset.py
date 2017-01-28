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

reset = False
for file in os.listdir(saves_dir):
    if file.endswith(".dat"):
        if "hunter.dat" == file.lower():
            reset = True
            os.remove(saves_dir + 'Hunter' + '.dat')
            
game_defs.init_char('Hunter', saves_dir)

if reset:
    print('Hunter reset.'.format())
else:
    print('Hunter created.')
