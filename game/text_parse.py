'''
Created on Dec 21, 2016

@author: Hunter Malm
'''

#from game import main
import pickle
from game_defs import print_by_char
from game_defs import save_game
from game_defs import display_prompt

# Text parse method
def parse_command(prompt, 
                  player, 
                  map_objects, 
                  item_objects,
                  saves_dir):
    # Parser input call and variables
    print_by_char(prompt, 0.01, False)
    raw_command = input().lower()
    print('------------------------------------------')
    raw_parts = raw_command.split()
    raw_word_count = len(raw_parts)
    fixed_parts = []
    
    
    actions = ["level",
               "journey",
               "health", 
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
               "save",
               "quit",
               "open",
               "visited"]
    active_actions = []
    
    arts = ["a",
            "an",
            "the"]
    active_arts = []
    
    locations = ['lab', 
                 'room', 
                 'dorm',
                 'club',
                 'lobby',
                 'hall']
    active_locs = []
    
    objs = ['phone',
            'laptop',
            'around',
            'door']
    active_objs = []
    
    adjs = ['south',
            'front',
            'dark',
            'wooden',
            'green',
            'blue',
            'red',
            'silver',
            'big',
            'left',
            'right']
    active_adjs = []
    
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
                
                
    # Add adjectives and adjective indexes to active_adjs list
    for i in range(len(fixed_parts)):
        for adj in adjs:
            if fixed_parts[i] == adj:
                active_adjs.append(fixed_parts[i])
                active_adjs.append(i)
                
    
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
        has_adj = [False]
        has_sec_adj = [False]
        
        # Check for article
        if int(active_actions[1] + 1) in active_arts:
            has_article[0] = True
            has_article.append(int(active_actions[1] + 1))
                
        
        # Check for adjective
        if has_article[0] == True:
            if (int(active_actions[1] + 2) in active_adjs):
                has_adj[0] = True
                has_adj.append(int(active_actions[1] + 2))
        else:
            if (int(active_actions[1] + 1) in active_adjs):
                has_adj[0] = True
                has_adj.append(int(active_actions[1] + 1))
                
        # Check for second adjective
        if has_adj[0] == True:
            if (int(active_adjs[1] + 1) in active_adjs):
                has_sec_adj[0] = True
                has_sec_adj.append(int(active_actions[1] + 2))
                
        
        if has_adj[0] == True:
            if has_adj[1] in active_objs or has_adj[1] in active_locs:
                if active_actions[0] == 'goto' or active_actions[0] == 'go' or active_actions[0] == 'move':
                    has_adj[0] = False      
                      
                
        # Check for direct object
        if has_article[0] == True and has_sec_adj[0] == True:
            if (int(active_actions[1] + 4) in active_objs) or (int(active_actions[1] + 4) in active_locs):
                has_dir_obj[0] = True
        if (has_article[0] == True and has_adj[0] == True) or (has_sec_adj[0] == True):
            if (int(active_actions[1] + 3) in active_objs) or (int(active_actions[1] + 3) in active_locs):
                has_dir_obj[0] = True
                has_dir_obj.append(int(active_actions[1] + 3))
        elif has_article[0] == True or has_adj[0] == True:
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
               
               
        if active_actions[0] == 'level':
            player.display_level()
        elif active_actions[0] == 'journey':
            player.display_journey()
        elif active_actions[0] == 'health':
            player.display_health()
        elif active_actions[0] == 'location':
            player.display_location()
        elif active_actions[0] == 'inventory':
            player.display_inventory()
        elif active_actions[0] == 'name':
            player.display_name()
        elif active_actions[0] == 'weight':
            player.display_weight()
        elif (active_actions[0] == 'stats') or (active_actions[0] == 'status') or (active_actions[0] == 'info'):
            player.display_stats()
        elif (active_actions[0] == 'goto') or (active_actions[0] == 'move') or (active_actions[0] == 'go'):
            location_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_locs, active_arts, active_adjs, player, envi, map_objects)
        elif active_actions[0] == 'take' or active_actions[0] == 'grab' or active_actions[0] == 'pickup' or active_actions[0] == 'pick':
            item_handle(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi)
        elif active_actions[0] == 'use':
            use_item(active_actions, has_article, has_dir_obj, active_objs, active_locs, active_arts, player, current_loc, envi, current_item)
        elif active_actions[0] == 'open':
            open_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_objs, active_arts, active_adjs, player, envi)
        elif active_actions[0] == 'clear':
            for i in range(100):
                print('')
        elif active_actions[0] == 'save':
            save_game(player, map_objects, item_objects, saves_dir)
        elif active_actions[0] == 'quit':
            return 'quit'
        elif active_actions[0] == 'look':
            look_handle(active_actions, has_dir_obj, active_objs, envi, player)
        elif active_actions[0] == 'visited':
            print(player.get_visited())
        else:
            print_by_char('Action not ready!', 0.01)
        
        active_actions.pop(0)
        active_actions.pop(0)
                    
                    
    if num_actv_actions == 0:
        print_by_char('Invalid command!', 0.01)
    

def look_handle(active_actions, has_dir_obj, active_objs, envi, player):
    # Update current prompt
    envi.update_current_prompt(envi.first_visit, envi.current_prompt, player)
    
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
    
    if has_dir_obj[0]:
            if active_objs[0] == 'around':
                display_prompt(envi, player)
                active_objs.pop(0)
                active_objs.pop(0)
                return
            else:
                print_by_char('Look at what?', 0.01)
    else:
        print_by_char('Look at what?', 0.01)
    
    
# Location handling method
def location_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_locs, active_arts, active_adjs, player, envi, map_objects):
    
    # Handles issue of removing locations from active_locs list when no action appears before it            
    while active_locs != []:
        if active_actions[1] > active_locs[1]:
            active_locs.pop(0)
            active_locs.pop(0)
            has_dir_obj[0] = False
        else:
            break
        
    
    if not active_locs:
        has_dir_obj[0] = False
    
    
    if  len(active_actions)/2 > active_actions.index(active_actions[0]) + 1:
        action_after = True
    else:
        action_after = False
    
    loc_found = False
    phrase = None
    
    if has_dir_obj[0]:
        
        # Build phrase based on number or lack of adjectives
        if has_sec_adj[0]:
            phrase = '{} {} {}'.format(active_adjs[0], active_adjs[2], active_locs[0])
        elif has_adj[0]:
            phrase = '{} {}'.format(active_adjs[0], active_locs[0])
        else:
            phrase = '{}'.format(active_locs[0])
            
        action_run = False
        
        
        for loc in envi.avail_locs:
            while not action_run:
                for name in loc:
                    if phrase == name:
                        envi = map_objects.get(loc[name])
                        player.set_location(action_after, envi, player)
                        action_run = True
                        loc_found = True
                break
        if not loc_found:
            print_by_char('>>> There is no {} available here.'.format(phrase), 0.01)
            
            if action_after:
                print('           --------------------')
                     
            
    else:
        
        # Since no direct objects exist, print question depending on the presence of an article
        if has_article[0]:
            print_by_char('{} {} what?'.format(active_actions[0], active_arts[0]), 0.01)
        else:
            print_by_char('{} where?'.format(active_actions[0]), 0.01)
            
    # Returns (removes the used adjs, arts, and objs)
    if has_article[0] and has_sec_adj[0] and has_dir_obj[0]:
        return active_arts.pop(0), active_arts.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_locs.pop(0), active_locs.pop(0)
    elif has_article[0] and has_adj[0] and has_dir_obj[0]:
        return active_arts.pop(0), active_arts.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_locs.pop(0), active_locs.pop(0)
    elif has_article[0] and has_dir_obj[0]:
        return active_arts.pop(0), active_arts.pop(0), active_locs.pop(0), active_locs.pop(0)
    elif has_sec_adj[0] and has_dir_obj[0]:
        return active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_locs.pop(0), active_locs.pop(0)
    elif has_adj[0] and has_dir_obj[0]:
        return active_adjs.pop(0), active_adjs.pop(0), active_locs.pop(0), active_locs.pop(0)
    elif has_dir_obj[0]:
        return active_locs.pop(0), active_locs.pop(0)


def open_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_objs, active_arts, active_adjs, player, envi):
    
    # Handles issue of removing locations from active_locs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
            has_dir_obj[0] = False
        else:
            break
        

    if not active_objs:
        has_dir_obj[0] = False
        
        
    if active_objs != []:
        if active_objs[0] != 'door':
            has_dir_obj[0] = False
            
            
    if  len(active_actions)/2 > active_actions.index(active_actions[0]) + 1:
        action_after = True
    else:
        action_after = False
    
    door_found = False
    phrase = None
    
    if has_dir_obj[0]:
        
        # Build phrase based on number or lack of adjectives
        if has_sec_adj[0]:
            phrase = '{} {} {}'.format(active_adjs[0], active_adjs[2], active_objs[0])
        elif has_adj[0]:
            phrase = '{} {}'.format(active_adjs[0], active_objs[0])
        else:
            phrase = '{}'.format(active_objs[0])
            
        # Check if the environment has any doors
        if envi.doors:
            open_run = False
            while not open_run:
                for door in envi.doors:
                    if phrase == door:
                        envi.open_door(phrase, action_after, player)
                        door_found = True
                        open_run = True
                break
            if not door_found:
                print_by_char('>>> There is no {} here.'.format(phrase), 0.01)
                
                if action_after:
                    print('           --------------------')
        else:
            print_by_char('>>> There are no doors here.', 0.01)
            
            if action_after:
                    print('           --------------------')
    else:
        
        # Since no direct objects exist, print question depending on the presence of an article
        if has_article[0]:
            print_by_char('{} {} what?'.format(active_actions[0], active_arts[0]), 0.01)
        else:
            print_by_char('{} what?'.format(active_actions[0]), 0.01)
            
    # Returns (removes the used adjs, arts, and objs)
    if has_article[0] and has_sec_adj[0] and has_dir_obj[0]:
        return active_arts.pop(0), active_arts.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_objs.pop(0), active_objs.pop(0)
    elif has_article[0] and has_adj[0] and has_dir_obj[0]:
        return active_arts.pop(0), active_arts.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_objs.pop(0), active_objs.pop(0)
    elif has_article[0] and has_dir_obj[0]:
        return active_arts.pop(0), active_arts.pop(0), active_objs.pop(0), active_objs.pop(0)
    elif has_sec_adj[0] and has_dir_obj[0]:
        return active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_adjs.pop(0), active_objs.pop(0), active_objs.pop(0)
    elif has_adj[0] and has_dir_obj[0]:
        return active_adjs.pop(0), active_adjs.pop(0), active_objs.pop(0), active_objs.pop(0)
    elif has_dir_obj[0]:
        return active_objs.pop(0), active_objs.pop(0)


# Location handling method
def item_handle(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
    
    # Handles issue of removing items from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1] or active_objs[0] == 'around':
            active_objs.pop(0)
            active_objs.pop(0)
            has_dir_obj[0] = False
        else:
            break
        
    
    if not active_objs:
        has_dir_obj[0] = False
    
    
    if has_article[0] == True:
        if has_dir_obj[0] == True:
            if is_item_at_location(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
                envi.remove_item(active_objs[0])
                player.add_item(active_objs[0], active_actions[0])
                return active_objs.pop(0), active_objs.pop(0), active_arts.pop(0), active_arts.pop(0)
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
                return active_objs.pop(0), active_objs.pop(0)
            else:
                print_by_char('>>> There is no ' + str(active_objs[0]) + ' here', 0.01)
        else:
            if active_actions[0] == 'pick':
                print_by_char(str(active_actions[0]) + ' up what?', 0.01)
            else:
                print_by_char(str(active_actions[0]) + ' what?', 0.01)
    
    
def is_item_at_location(active_actions, has_article, has_dir_obj, active_objs, active_arts, player, current_loc, envi):
    
    if current_loc == envi.get_name():
        if active_objs[0] in envi.get_inventory():
            return True
        else:
            return False
    else:
        return False
    

def use_item(active_actions, has_article, has_dir_obj, active_objs, active_locs, active_arts, player, current_loc, envi, current_item):
    
    # Handles issue of removing items from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1] or active_objs[0] == 'around':
            active_objs.pop(0)
            active_objs.pop(0)
            has_dir_obj[0] = False
        else:
            break
    
    if not active_objs:
        has_dir_obj[0] = False
        
        
    if has_article[0] == True:
        if has_dir_obj[0] == True:
            if is_item_in_inventory(active_objs, player):
                current_item.use()
                #print('Used the item..')
                return active_objs.pop(0), active_objs.pop(0), active_arts.pop(0), active_arts.pop(0)
            else:
                print('>>> You don\'t have a ' + str(active_objs[0]))
        else:
            print(str(active_actions[0]) + ' ' + str(active_arts[0]) + ' what?')
                
                
    else:
        if has_dir_obj[0] == True:
            if is_item_in_inventory(active_objs, player):
                current_item.use()
                #print('Used item..')
                return active_objs.pop(0), active_objs.pop(0)
            else:
                print('>>> {} doesn\'t have a {}.'.format(player.get_name(), active_objs[0]))
        else:
            print(str(active_actions[0]) + ' what?')


def is_item_in_inventory(active_objs, player):
    
    if active_objs[0] in player.get_inventory():
        #print('Player has item')
        return True
    else:
        #print('Player does not have item')
        return False


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
