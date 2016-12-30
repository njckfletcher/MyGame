'''
Created on Dec 21, 2016

@author: Hunter Malm
'''

#from game import main
import pickle
from game.game_defs import print_by_char

# Text parse method
def parse_command(prompt, 
                  player, 
                  current_loc, 
                  map_objects, 
                  item_objects):
    # Parser input call and variables
    print_by_char(prompt, 0.01, False)
    raw_command = input().lower()
    print('------------------------------------------')
    raw_parts = raw_command.split()
    raw_word_count = len(raw_parts)
    fixed_parts = []
    
    
    actions = ["health", 
               "inventory", 
               "location",
               "name", 
               "weight", 
               "goto", 
               "move",
               "go",
               "look",
               "take",
               "pickup",
               "pick",
               "grab",
               "clear",
               "change",
               "stats",
               "status",
               "info",
               "use",
               "save"]
    active_actions = []
    
    arts = ["a",
            "an",
            "the"]
    active_arts = []
    
    locations = ['lab', 
                 'room', 
                 'dorm',
                 'club']
    active_locs = []
    
    objs = ['phone']
    active_objs = []
    
    filter_words = ['to',
                    'display',
                    'my',
                    'up',
                    'and']
    
    
    for word in raw_parts:
        fixed_parts.append(word)
    
    
    # Remove filler words from fixed_parts and set count
    fixed_parts = [x for x in fixed_parts if x not in filter_words]
    fixed_word_count = len(fixed_parts)            
                
    # Add actions and action indexes to active_actions list
    for i in range(len(fixed_parts)):
        for action in actions:
            if fixed_parts[i] == action:
                active_actions.append(fixed_parts[i])
                active_actions.append(i)
                
    
    # Find number of actions
    num_actv_actions = int(len(active_actions)/2)
    
    
    # Add articles and article indexes to active_arts list
    for i in range(len(fixed_parts)):
        for art in arts:
            if fixed_parts[i] == art:
                active_arts.append(fixed_parts[i])
                active_arts.append(i)   
    
    
    # Add locations and location indexes to active_locs list
    for i in range(len(fixed_parts)):
        for location in locations:
            if fixed_parts[i] == location:
                active_locs.append(fixed_parts[i])
                active_locs.append(i)
                
    
    # Add objects and object indexes to active_objs list
    for i in range(len(fixed_parts)):
        for obj in objs:
            if fixed_parts[i] == obj:
                active_objs.append(fixed_parts[i])
                active_objs.append(i)
                
                
    ##########################################
    # DEBUGGING COMMAND METHOD
    #debug_command(raw_parts, raw_word_count, fixed_parts, fixed_word_count, active_actions, num_actv_actions, active_arts, active_locs, active_objs)
    
    
    # Running possibilities based on number of actions called
    for i in range(num_actv_actions):
        current_loc = player.get_location()
        envi = map_objects.get(player.location)
        if active_objs != []:
            current_item = item_objects.get(active_objs[0])
        else:
            current_item = None
        has_article = [False]
        has_dir_obj = [False]
        
        # Check for article
        if int(active_actions[1] + 1) in active_arts:
            has_article[0] = True
            has_article.append(int(active_actions[1] + 1))
            
        
        # Check for direct object
        if has_article[0] == True:
            if (int(active_actions[1] + 2) in active_objs) or (int(active_actions[1] + 2) in active_locs):
                has_dir_obj[0] = True
                has_dir_obj.append(int(active_actions[1] + 2))
        else:
            if (int(active_actions[1] + 1) in active_objs) or (int(active_actions[1] + 1) in active_locs):
                has_dir_obj[0] = True
                has_dir_obj.append(int(active_actions[1] + 1))
                
        
        ##########################################
        # DEBUGGING PER ACTION METHOD:        
        #debug_arts_objs(active_actions, has_article, has_dir_obj)
               
               
        if active_actions[0] == 'health':
            player.display_health()
            active_actions.pop(0)
            active_actions.pop(0)
        elif active_actions[0] == 'location':
            player.display_location()
            active_actions.pop(0)
            active_actions.pop(0)
        elif active_actions[0] == 'inventory':
            player.display_inventory()
            active_actions.pop(0)
            active_actions.pop(0)
        elif active_actions[0] == 'name':
            player.display_name()
            active_actions.pop(0)
            active_actions.pop(0)
        elif active_actions[0] == 'weight':
            player.display_weight()
            active_actions.pop(0)
            active_actions.pop(0)
        elif (active_actions[0] == 'stats') or (active_actions[0] == 'status') or (active_actions[0] == 'info'):
            player.display_stats()
            active_actions.pop(0)
            active_actions.pop(0)
        elif (active_actions[0] == 'goto') or (active_actions[0] == 'move') or (active_actions[0] == 'go'):
            location_handle(active_actions, has_article, has_dir_obj, active_locs, active_arts, player)
        elif active_actions[0] == 'take' or active_actions[0] == 'grab' or active_actions[0] == 'pickup' or active_actions[0] == 'pick':
            item_handle(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi)
        elif active_actions[0] == 'use':
            use_item(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi, current_item)
        elif active_actions[0] == 'clear':
            for i in range(100):
                print('')
            active_actions.pop(0)
            active_actions.pop(0)
        elif active_actions[0] == 'save':
            save_game(player, map_objects, item_objects)
            active_actions.pop(0)
            active_actions.pop(0)
        else:
            print_by_char('Action not ready!', 0.01)
                    
                    
    if num_actv_actions == 0:
        print_by_char('Invalid command!', 0.01)
    

# Location handling method
def location_handle(active_actions, has_article, has_dir_obj, active_locs, active_arts, player):
    
    # Handles issue of removing locations from active_locs list when no action appears before it            
    while active_locs != []:
        if active_actions[1] > active_locs[1]:
            active_locs.pop(0)
            active_locs.pop(0)
        else:
            break
    
    
    if has_article[0] == True:
        if has_dir_obj[0] == True:
            player.set_location(active_locs[0])
            return active_actions.pop(0), active_actions.pop(0), active_locs.pop(0), active_locs.pop(0), active_arts.pop(0), active_arts.pop(0)
        else:
            if active_actions[0] == 'goto':
                print_by_char(str(active_actions[0]) + ' ' + str(active_arts[0]) + ' what?', 0.01)
            else:
                print_by_char(str(active_actions[0]) + ' to ' + str(active_arts[0]) + ' what?', 0.01)
    else:
        if has_dir_obj[0] == True:
            player.set_location(active_locs[0])
            return active_actions.pop(0), active_actions.pop(0), active_locs.pop(0), active_locs.pop(0)
        else:
            print_by_char(str(active_actions[0]) + ' where?', 0.01)
           
    return active_actions.pop(0), active_actions.pop(0)


# Location handling method
def item_handle(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
    
    # Handles issue of removing items from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
        
        
    if has_article[0] == True:
        if has_dir_obj[0] == True:
            if is_item_at_location(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
                envi.remove_item(active_objs[0])
                player.add_item(active_objs[0], active_actions[0])
                return active_actions.pop(0), active_actions.pop(0), active_objs.pop(0), active_objs.pop(0), active_arts.pop(0), active_arts.pop(0)
            else:
                print_by_char('>>> There is no ' + str(active_objs[0]) + ' here', 0.01)
        else:
            if active_actions[0] == 'pick':
                print_by_char(str(active_actions[0]) + ' up ' + str(active_arts[0]) + ' what?', 0.01)
            else:
                print_by_char(str(active_actions[0]) + ' ' + str(active_arts[0]) + ' what?', 0.01)
                
                
    else:
        if has_dir_obj[0] == True:
            if is_item_at_location(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
                envi.remove_item(active_objs[0])
                player.add_item(active_objs[0], active_actions[0])
                return active_actions.pop(0), active_actions.pop(0), active_objs.pop(0), active_objs.pop(0)
            else:
                print_by_char('>>> There is no ' + str(active_objs[0]) + ' here', 0.01)
        else:
            if active_actions[0] == 'pick':
                print_by_char(str(active_actions[0]) + ' up what?', 0.01)
            else:
                print_by_char(str(active_actions[0]) + ' what?', 0.01)
            
            
    return active_actions.pop(0), active_actions.pop(0)
    
    
def is_item_at_location(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
    
    if current_loc == envi.get_name():
        if active_objs[0] in envi.get_inventory():
            return True
        else:
            return False
    else:
        return False
    

def use_item(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi, current_item):
    
    # Handles issue of removing items from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
        
        
    if has_article[0] == True:
        if has_dir_obj[0] == True:
            if is_item_in_inventory(active_objs, player):
                current_item.use()
                #print('Used the item..')
                return active_actions.pop(0), active_actions.pop(0), active_objs.pop(0), active_objs.pop(0), active_arts.pop(0), active_arts.pop(0)
            else:
                print('>>> You dont have a ' + str(active_objs[0]))
        else:
            print(str(active_actions[0]) + ' ' + str(active_arts[0]) + ' what?')
                
                
    else:
        if has_dir_obj[0] == True:
            if is_item_in_inventory(active_objs, player):
                current_item.use()
                #print('Used item..')
                return active_actions.pop(0), active_actions.pop(0), active_objs.pop(0), active_objs.pop(0)
            else:
                print('>>> You dont have a ' + str(active_objs[0]))
        else:
            print(str(active_actions[0]) + ' what?')
            
            
    return active_actions.pop(0), active_actions.pop(0)


def is_item_in_inventory(active_objs, player):
    
    if active_objs[0] in player.get_inventory():
        #print('Player has item')
        return True
    else:
        #print('Player does not have item')
        return False
    

def save_game(player, map_objects, item_objects):
    with open('savefile.dat', 'wb') as f:
        pickle.dump([player, map_objects, item_objects], f, protocol=4)


def debug_command(raw_parts, raw_word_count, fixed_parts, fixed_word_count, active_actions, num_actv_actions, active_arts, active_locs, active_objs):
    print('##########################################')
    print('DEBUGGING INPUT:')
    print('>>> Raw Parts: ' + str(raw_parts))
    print('>>> Number of raw words: ' + str(raw_word_count))
    print('>>> Fixed Parts: ' + str(fixed_parts))
    print('>>> Number of fixed words: ' + str(fixed_word_count))
    print('>>> Active actions: ' + str(active_actions))
    print('>>> Number of active actions: ' + str(num_actv_actions))
    print('>>> Active articles: ' + str(active_arts))
    print('>>> Active locations: ' + str(active_locs))
    print('>>> Active objects: ' + str(active_objs))
    print('##########################################')
    

def debug_arts_objs(active_actions, has_article, has_dir_obj):
    print('##########################################')
    print('DEBUGGING PER ACTION:')
    print('>>> Does ' + str(active_actions[0]) + ' have an article?: ' + str(has_article))
    print('>>> Does ' + str(active_actions[0]) + ' have a direct object?: ' + str(has_dir_obj))
    print('##########################################')
