'''
Created on Dec 31, 2016

@author: Hunter Malm
'''
import game_objects
from game_defs import print_by_char

lobby = game_objects.FB_lobby()

for i in range(len(lobby.current_prompt)):
    for line in lobby.current_prompt[i]:
        print_by_char(line, 0.01)
    print('')
    

print('------------------------------------------')
lobby.new_prompt(lobby.first_visit, lobby.current_prompt)

for i in range(len(lobby.current_prompt)):
    for line in lobby.current_prompt[i]:
        print_by_char(line, 0.01)
    print('')
    

print('------------------------------------------')
lobby.new_prompt(lobby.first_visit, lobby.current_prompt)

for i in range(len(lobby.current_prompt)):
    for line in lobby.current_prompt[i]:
        print_by_char(line, 0.01)
    print('')