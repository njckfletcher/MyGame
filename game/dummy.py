'''
Created on Dec 31, 2016

@author: Hunter Malm
'''
from game import game_objects

lobby = game_objects.FB_lobby()

#print(lobby.south_hall_door.open)
#lobby.open_door('south hall door')
#print(lobby.south_hall_door.open)
#print(lobby.south_hall_door.open)



print(lobby.get_avail_locs())
print(lobby.get_avail_locs())
print(lobby.get_avail_locs())
lobby.open_door('south hall door')
print(lobby.get_avail_locs())
lobby.open_door('south hall door')
print(lobby.get_avail_locs())