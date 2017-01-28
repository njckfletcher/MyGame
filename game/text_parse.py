'''
Created on Dec 21, 2016

@author: Hunter Malm
'''

#from game import main
import pickle, os
from game_defs import print_by_char, save_game, display_prompt
from profanity import profanity

# Text parse method
def parse_command(prompt, 
                  player, 
                  map_objects,
                  saves_dir,
                  just_saved):
    # Parser input call and variables
    print_by_char(prompt, 0.005, False)
    raw_command = input().lower()
    contains_profanity = profanity.contains_profanity(raw_command)
    print('--------------------------------------------')
    
    if contains_profanity:
        player.receive_damage(20)
        print_by_char('>>> 20 point penalty for using profanity!', 0.005)
        raw_command = ''
        
    raw_parts = raw_command.split()
    raw_word_count = len(raw_parts)
    fixed_parts = []
    
    loc_actions = ['goto',
                   'go',
                   'move']
    
    obj_actions = ['take',
                   'grab',
                   'pick',
                   'pickup',
                   'open',
                   'use',
                   'look',
                   'put',
                   'place']
    
    actions = ["level",
               "journey",
               "health", 
               "inventory", 
               "location",
               "name", 
               "weight",
               "clear",
               "change",
               "stats",
               "status",
               "info",
               "save",
               "quit",
               "unlock",
               "visited",]
    
    for loc_action in loc_actions:
        actions.append(loc_action)
        
    for obj_action in obj_actions:
        actions.append(obj_action)
    
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
            'door',
            'locker']
    active_objs = []
    
    adjs = ["south",
            "front",
            "dark",
            "wooden",
            "green",
            "blue",
            "red",
            "silver",
            "big",
            "left",
            "right",
            "shiny",
            "old",
            "forbidden",
            "random",
            "desperation",
            "gentlemans",
            "gentleman's"]
    active_adjs = []
    
    preps = ['in',
             'from']
    active_preps = []
    
    filter_words = ['to',
                    'display',
                    'my',
                    'up',
                    'and']
    
    # Remove filler words from fixed_parts and set count
    fixed_parts = [x for x in raw_parts if x not in filter_words]
    fixed_word_count = len(fixed_parts)   
    
    
    # Specials
    for i in range(len(fixed_parts)):
        if fixed_parts[i] == "gentlemans":
            fixed_parts[i] = "gentleman's"      
                
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
                
    
    # Add prepositions and preposition indexes to active_preps list
    for i in range(len(fixed_parts)):
        for prep in preps:
            if fixed_parts[i] == prep:
                active_preps.append(fixed_parts[i])
                active_preps.append(i)
                
    
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
                
    
    saved = False
    for action in active_actions:
        if action == 'save':
            saved = True
                
                
    ##########################################
    # DEBUGGING COMMAND METHOD
    #debug_command(raw_parts, raw_word_count, fixed_parts, fixed_word_count, active_actions, num_actv_actions, active_arts, active_locs, active_objs)
    
    actions_run = 0
    # Running possibilities based on number of actions called
    for i in range(num_actv_actions):
        
        if not active_actions:
            break
        
        current_loc = player.get_location()
        envi = map_objects.get(player.get_location())
        has_article = [False]
        has_dir_obj = [False]
        has_adj = [False]
        has_sec_adj = [False]
        has_prep = [False]
        has_prep_art = [False]
        has_prep_obj = [False]
        has_prep_adj = [False]
        has_sec_prep_adj = [False]
        obj_of_prep = None
        
        action_after = is_action_after(active_actions)        
        
        # Check for article
        if active_actions[1] + 1 in active_arts:
            has_article[0] = True
            has_article.append(active_actions[1] + 1)
                
        
        # Check for adjective
        if has_article[0] == True:
            if active_actions[1] + 2 in active_adjs:
                has_adj[0] = True
                has_adj.append(active_actions[1] + 2)
        else:
            if active_actions[1] + 1 in active_adjs:
                has_adj[0] = True
                has_adj.append(active_actions[1] + 1)
                
        # Check for second adjective
        if has_adj[0] == True:
            if active_adjs[1] + 1 in active_adjs:
                has_sec_adj[0] = True
                has_sec_adj.append(active_actions[1] + 2)
                
                
        # Check for direct object
        if has_article[0] == True and has_sec_adj[0] == True:
            if active_actions[0] in loc_actions:
                if active_actions[1] + 4 in active_locs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 4)
            elif active_actions[0] in obj_actions:
                if active_actions[1] + 4 in active_objs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 4)
        elif (has_article[0] == True and has_adj[0] == True) or (has_sec_adj[0] == True):
            if active_actions[0] in loc_actions:
                if active_actions[1] + 3 in active_locs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 3)
            elif active_actions[0] in obj_actions:
                if active_actions[1] + 3 in active_objs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 3)
        elif has_article[0] == True or has_adj[0] == True:
            if active_actions[0] in loc_actions:
                if active_actions[1] + 2 in active_locs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 2)
            elif active_actions[0] in obj_actions:
                if active_actions[1] + 2 in active_objs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 2)
        else:
            if active_actions[0] in loc_actions:
                if active_actions[1] + 1 in active_locs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 1)
            elif active_actions[0] in obj_actions:
                if active_actions[1] + 1 in active_objs:
                    has_dir_obj[0] = True
                    has_dir_obj.append(active_actions[1] + 1)
                    
        # Check for preposition
        if has_dir_obj[0] == True:
            if has_dir_obj[1] + 1 in active_preps:
                has_prep[0] = True
                has_prep.append(has_dir_obj[1] + 1)
                
        # Check for preposition article
        if has_prep[0] == True:
            if has_prep[1] + 1 in active_arts:
                has_prep_art[0] = True
                has_prep_art.append(has_prep[1] + 1)
                
        # Check for preposition adjective
        if has_prep[0] == True:
            if has_prep_art[0]:
                if has_prep_art[1] + 1 in active_adjs:
                    has_prep_adj[0] = True
                    has_prep_adj.append(has_prep_art[1] + 1)
                    
            elif has_prep[1] + 1 in active_adjs:
                has_prep_adj[0] = True
                has_prep_adj.append(has_prep[1] + 1)
            
                
        # Check for second preposition adjective
        if has_prep_adj[0] == True:
            if has_prep_adj[1] + 1 in active_adjs:
                has_sec_prep_adj[0] = True
                has_sec_prep_adj.append(has_prep_adj[1] + 1)

                
        # Check for object of preposition (only if it has a preposition)
        if has_prep[0] == True:
            if has_prep_art[0]:
                if has_sec_prep_adj[0] == True:
                    if has_sec_prep_adj[1] + 1 in active_objs:
                        has_prep_obj[0] = True
                        has_prep_obj.append(has_sec_prep_adj[1] + 1)
                
                elif has_prep_adj[0] == True:
                    if has_prep_adj[1] + 1 in active_objs:
                        has_prep_obj[0] = True
                        has_prep_obj.append(has_prep_adj[1] + 1)
                        
                elif has_prep_art[1] + 1 in active_objs:
                    has_prep_obj[0] = True
                    has_prep_obj.append(has_prep_art[1] + 1)
                
            else:
                if has_sec_prep_adj[0] == True:
                    if has_sec_prep_adj[1] + 1 in active_objs:
                        has_prep_obj[0] = True
                        has_prep_obj.append(has_sec_prep_adj[1] + 1)
                
                elif has_prep_adj[0] == True:
                    if has_prep_adj[1] + 1 in active_objs:
                        has_prep_obj[0] = True
                        has_prep_obj.append(has_prep_adj[1] + 1)
                        
                elif has_prep[1] + 1 in active_objs:
                    has_prep_obj[0] = True
                    has_prep_obj.append(has_prep[1] + 1)
                    
                    
        if has_prep_obj[0]:
            if has_sec_prep_adj[0]:
                if has_sec_adj[0]:
                    obj_of_prep = '{} {} {}'.format(active_adjs[4], active_adjs[6], active_objs[2])
                elif has_adj[0]:
                    obj_of_prep = '{} {} {}'.format(active_adjs[2], active_adjs[4], active_objs[2])
                else:
                    obj_of_prep = '{} {} {}'.format(active_adjs[0], active_adjs[2], active_objs[2])
            elif has_prep_adj[0]:
                if has_sec_adj[0]:
                    obj_of_prep = '{} {}'.format(active_adjs[4], active_objs[2])
                elif has_adj[0]:
                    obj_of_prep = '{} {}'.format(active_adjs[2], active_objs[2])
                else:
                    obj_of_prep = '{} {}'.format(active_adjs[0], active_objs[2])
            else:
                obj_of_prep = '{}'.format(active_objs[2])
                
        # DEBUGGING PER ACTION METHOD:        
        #debug_action(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, has_prep, has_prep_art, has_prep_adj, has_sec_prep_adj, has_prep_obj) 
               
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
            location_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_locs, active_arts, active_adjs, player, envi, map_objects, locations)
        elif active_actions[0] == 'take' or active_actions[0] == 'grab' or active_actions[0] == 'pickup' or active_actions[0] == 'pick':
            item_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, has_prep, has_prep_obj, has_prep_art, active_objs, active_arts, active_adjs, active_preps, player, current_loc, envi, obj_of_prep)
        elif active_actions[0] == 'use':
            use_item(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_objs, active_arts, active_adjs, player, envi)
        elif active_actions[0] == 'open':
            open_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_objs, active_arts, active_adjs, player, envi)
        elif active_actions[0] == 'put' or active_actions[0] == 'place':
            put_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, has_prep, has_prep_obj, has_prep_art, active_objs, active_arts, active_adjs, active_preps, player, current_loc, envi, obj_of_prep)
        elif active_actions[0] == 'clear':
            for i in range(100):
                print('')
        elif active_actions[0] == 'save':
            save_game(player, map_objects, saves_dir)
            saved = True
        elif active_actions[0] == 'quit':
            if not saved and just_saved == False:
                save_before_quit(player, map_objects, saves_dir)
                print('')
            return 'quit'
        elif active_actions[0] == 'look':
            look_handle(active_actions, has_dir_obj, active_objs, envi, player)
        elif active_actions[0] == 'visited':
            print(player.get_visited())
        elif active_actions[0] == 'change':
            change_name(saves_dir, active_actions, player, map_objects)
        else:
            print_by_char('Action not ready!', 0.005)
            
        if action_after: print('          ----------------------')
        
        # Removes the used adjs, arts, preps, and objs
        if has_article[0]:
            active_arts.pop(0)
            active_arts.pop(0)
        if has_dir_obj[0]:
            if active_actions[0] in loc_actions:
                active_locs.pop(0)
                active_locs.pop(0)
            elif active_actions[0] in obj_actions:
                active_objs.pop(0)
                active_objs.pop(0)
        if has_adj[0]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        if has_sec_adj[0]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        if has_prep[0]:
            active_preps.pop(0)
            active_preps.pop(0)
        if has_prep_art[0]:
            active_arts.pop(0)
            active_arts.pop(0)
        if has_prep_obj[0]:
            active_objs.pop(0)
            active_objs.pop(0)
        if has_prep_adj[0]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        if has_sec_prep_adj[0]:
            active_adjs.pop(0)
            active_adjs.pop(0)
            
        active_actions.pop(0)
        active_actions.pop(0)
                    
    if num_actv_actions == 0 and not contains_profanity:
        print_by_char('Invalid command!', 0.005)
        
    if saved:
        return 'saved'
    else:
        return 'not saved'
    

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
                
            else:
                print_by_char('Look at what?', 0.005)
    else:
        print_by_char('Look at what?', 0.005)
    
    
# Location handling method
def location_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_locs, active_arts, active_adjs, player, envi, map_objects, locations):
    # Handles issue of removing locations from active_locs list when the current action appears after it        
    while active_locs != []:
        if active_actions[1] > active_locs[1]:
            active_locs.pop(0)
            active_locs.pop(0)
            
        else:
            break
       
    # Handles issue of removing adjectives from active_adjs list when the current action appears after it
    while active_adjs != []:
        if active_actions[1] > active_adjs[1]:
            active_adjs.pop(0)
            active_adjs.pop(0)
            
        else:
            break
        
    if not active_locs:
        has_dir_obj[0] = False
        
    if active_locs:
        if active_locs[0] not in locations:
            has_dir_obj[0] = False
    
    
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
                        player.set_location(envi, player, phrase)
                        action_run = True
                        loc_found = True
                break
        if not loc_found:
            print_by_char('>>> There is no {} available here.'.format(phrase), 0.005)
                     
            
    else:
        
        # Since no direct objects exist, print question depending on the presence of an article
        if has_article[0]:
            if active_actions[0] == 'goto':
                print_by_char('{} {} what?'.format(active_actions[0], active_arts[0]), 0.005)
            else:
                print_by_char('{} to {} what?'.format(active_actions[0], active_arts[0]), 0.005)
        else:
            print_by_char('{} where?'.format(active_actions[0]), 0.005)


def open_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_objs, active_arts, active_adjs, player, envi):
    # Handles issue of removing objects from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
    
    while active_adjs != []:
        if active_actions[1] > active_adjs[1]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        else:
            break
        

    if not active_objs:
        has_dir_obj[0] = False
        
        
    if active_objs != []:
        if active_objs[0] != 'door':
            has_dir_obj[0] = False
            
    
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
                        envi.open_door(phrase, player)
                        door_found = True
                        open_run = True
                break
            if not door_found:
                print_by_char('>>> There is no {} here.'.format(phrase), 0.005)
        else:
            print_by_char('>>> There are no doors here.', 0.005)
            
    else:
        
        # Since no direct objects exist, print question depending on the presence of an article
        if has_article[0]:
            print_by_char('{} {} what?'.format(active_actions[0], active_arts[0]), 0.005)
        else:
            print_by_char('{} what?'.format(active_actions[0]), 0.005)


# Location handling method
def item_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, has_prep, has_prep_obj, has_prep_art, active_objs, active_arts, active_adjs, active_preps, player, current_loc, envi, obj_of_prep):
    takable_items = ['laptop',
                    'phone']
    # Handles issue of removing objects from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
    
    while active_adjs != []:
        if active_actions[1] > active_adjs[1]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        else:
            break
        

    if not active_objs:
        has_dir_obj[0] = False
        
    
    if active_objs:
        if active_objs[0] not in takable_items:
            has_dir_obj[0] = False
            
    if active_actions[0] == 'take':
        past_action = 'took'
    elif active_actions[0] == 'grab':
        past_action = 'grabbed'
    else:
        past_action = 'picked up'
        active_actions[0] = 'pick up'
    
    container_found = False
    item_found = False
    phrase = None
    take_run = False
    
    if has_dir_obj[0]:
        if has_sec_adj[0]:
            phrase = '{} {} {}'.format(active_adjs[0], active_adjs[2], active_objs[0])
                        
        elif has_adj[0]:
            phrase = '{} {}'.format(active_adjs[0], active_objs[0])
                        
        else:
            phrase = '{}'.format(active_objs[0])
        
        if has_prep[0]:
            if has_prep_obj[0]:
                if envi.containers:
                    containers = envi.containers
                    
                    for container in containers:
                        if container == obj_of_prep:
                            container_found = True
                            inventory = containers[container].get_inventory()
                            while not take_run:
                                for item in inventory:
                                    if phrase == item:
                                        item_found = True
                                        take_run = True
                                        player.add_item(phrase, inventory[phrase])
                                        envi.containers[container].remove_item(phrase)
                                        print_by_char('>>> {} {} the {} {} the {}.'.format(player.get_name(), past_action, phrase, active_preps[0], obj_of_prep), 0.005)
                                        break
                                            
                                if not item_found:
                                    print_by_char('There is no {} in the {}.'.format(phrase, obj_of_prep), 0.005)
                                    break
                                        
                    if not container_found:
                        print_by_char('There is no {} here.'.format(obj_of_prep), 0.005)
                                
                else:
                    print_by_char('There is no {} here.'.format(obj_of_prep), 0.005)
            else:
                print_by_char('>>> {} the {} {} the what?'.format(active_actions[0], phrase, active_preps[0]), 0.005)
        else:
            if envi.inventory:
                inventory = envi.inventory
                
                while not take_run:
                    for item in inventory:
                        if phrase == item:
                            item_found = True
                            take_run = True
                            player.add_item(phrase, inventory[phrase])
                            envi.remove_item(phrase)
                            print_by_char('>>> {} {} the {}.'.format(player.get_name(), past_action, phrase), 0.005)
                            break
                    
            if not item_found:
                print_by_char('There is no {} here.'.format(phrase), 0.005)
        
    else:
        print_by_char('{} what?'.format(active_actions[0]), 0.005)    
    
    
def put_handle(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, has_prep, has_prep_obj, has_prep_art, active_objs, active_arts, active_adjs, active_preps, player, current_loc, envi, obj_of_prep):
    placable_items = ['laptop',
                    'phone']
    # Handles issue of removing objects from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
    
    while active_adjs != []:
        if active_actions[1] > active_adjs[1]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        else:
            break
        

    if not active_objs:
        has_dir_obj[0] = False
        
    
    if active_objs:
        if active_objs[0] not in placable_items:
            has_dir_obj[0] = False
            
            
    container_found = False
    item_found = False
    phrase = None
    
    if has_dir_obj[0]:
        # Build phrase based on number or lack of adjectives
        if has_sec_adj[0]:
            phrase = '{} {} {}'.format(active_adjs[0], active_adjs[2], active_objs[0])
                        
        elif has_adj[0]:
            phrase = '{} {}'.format(active_adjs[0], active_objs[0])
                        
        else:
            phrase = '{}'.format(active_objs[0])
        
        if has_prep[0]:
            if has_prep_obj[0]:
                # Check if the player has any items
                if player.get_inventory():
                    put_run = False
                    
                    while not put_run:
                        for item in player.get_inventory():
                            if phrase == item:
                                item_found = True
                                for container in envi.containers:
                                    if obj_of_prep == container:
                                        container_found = True
                                        envi.containers[obj_of_prep].add_item(item, player.get_inventory()[item], player, active_actions, obj_of_prep)
                                        del player.get_inventory()[item]
                                        player.sub_weight(envi.containers[obj_of_prep].inventory[phrase].get_weight())
                                        put_run = True
                                        break
                                if not container_found:
                                    print_by_char('>>> There is no {} here.'.format(obj_of_prep), 0.005)
                                break
                                    
                        if not item_found:
                            print_by_char('>>> You have no {}.'.format(phrase), 0.005)
                        break
                else:
                    print_by_char('>>> You have no items.', 0.005)
                    
            else:
                for item in player.get_inventory():
                    if phrase == item:
                        item_found = True
                        
                if not item_found:
                    print_by_char('>>> You have no {}.'.format(phrase), 0.005)
                elif has_article[0]:
                    if has_prep_art[0]:
                        print_by_char('{} {} {} {} {} what?'.format(active_actions[0], active_arts[0], phrase, active_preps[0], active_arts[2]), 0.005)
                    else:
                        print_by_char('{} {} {} {} what?'.format(active_actions[0], active_arts[0], phrase, active_preps[0]), 0.005)
                else:
                    if has_prep_art[0]:
                        print_by_char('{} {} {} {} what?'.format(active_actions[0], phrase, active_preps[0], active_arts[0]), 0.005)
                    else:
                        print_by_char('{} {} {} what?'.format(active_actions[0], phrase, active_preps[0]), 0.005)
                
        else:
            for item in player.get_inventory():
                if phrase == item:
                    item_found = True
                    
            if not item_found:
                print_by_char('>>> You have no {}.'.format(phrase), 0.005)
            elif has_article[0]:
                print_by_char('{} {} {} where?'.format(active_actions[0], active_arts[0], phrase), 0.005)
            else:
                print_by_char('{} {} where?'.format(active_actions[0], phrase), 0.005)
                
    else:
        # Since no direct objects exist, print question depending on the presence of an article
        if has_article[0]:
            print_by_char('{} {} what where?'.format(active_actions[0], active_arts[0]), 0.005)
        else:
            print_by_char('{} what where?'.format(active_actions[0]), 0.005)
    

def use_item(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, active_objs, active_arts, active_adjs, player, envi):
    usable_items = ['laptop',
                    'phone']
    # Handles issue of removing objects from active_objs list when no action appears before it
    while active_objs != []:
        if active_actions[1] > active_objs[1]:
            active_objs.pop(0)
            active_objs.pop(0)
        else:
            break
    
    while active_adjs != []:
        if active_actions[1] > active_adjs[1]:
            active_adjs.pop(0)
            active_adjs.pop(0)
        else:
            break
        

    if not active_objs:
        has_dir_obj[0] = False
        
    
    if active_objs:
        if active_objs[0] not in usable_items:
            has_dir_obj[0] = False
    
            
    
    item_found = False
    phrase = None
    
    if has_dir_obj[0]:
        
        # Build phrase based on number or lack of adjectives
        if has_sec_adj[0]:
            phrase = '{} {} {}'.format(active_adjs[0], active_adjs[2], active_objs[0])
        elif has_adj[0]:
            phrase = '{} {}'.format(active_adjs[0], active_objs[0])
        else:
            phrase = '{}'.format(active_objs[0])
            
        # Check if the player has any items
        if player.get_inventory():
            use_run = False
            while not use_run:
                for item in player.get_inventory():
                    if phrase == item:
                        player.get_inventory()[phrase].use()
                        item_found = True
                        use_run = True
                break
            if not item_found:
                print_by_char('>>> There is no {} in your inventory.'.format(phrase), 0.005)
        else:
            print_by_char('>>> You do not have any items to use.', 0.005)
            
    else:
        
        # Since no direct objects exist, print question depending on the presence of an article
        if has_article[0]:
            print_by_char('{} {} what?'.format(active_actions[0], active_arts[0]), 0.005)
        else:
            print_by_char('{} what?'.format(active_actions[0]), 0.005)
    
    
def is_action_after(active_actions):
    # The following actions list contains the actions that gets a line printed before or after them in the presence of another action
    actions = ['open',
               'goto',
               'go',
               'move',
               'look',
               'info',
               'stats',
               'status',
               'use',
               'change',
               'inventory',
               'put',
               'place',
               'take',
               'grab',
               'pick',
               'pickup',
               'quit']
    
    # Specials
    if  len(active_actions)/2 > active_actions.index(active_actions[0]) + 1:
        if active_actions[0] == 'change' and active_actions[2] == 'name':
            if len(active_actions)/2 > 2:
                return True
            return False
    
    # Main
    for action in actions:
        if active_actions[0] == action:
            if  len(active_actions)/2 > active_actions.index(active_actions[0]) + 1:
                return True
        else:
            if  len(active_actions)/2 > active_actions.index(active_actions[0]) + 1:
                if active_actions[2] == action:
                    return True
    return False


def change_name(saves_dir, active_actions, player, map_objects):
    if len(active_actions) > 2:
        if active_actions[2] == 'name':
            print_by_char('What would you like to change your name to?', 0.005)
            current_name = player.get_name()
            print_by_char('Current name: {}'.format(current_name), 0.005)
            name_set = False
            while not name_set:
                name_taken = False
                print_by_char('New name: ', 0.005, False)
                new_name = input()
                if new_name == current_name:
                    print('')
                    print_by_char("> Your name is already {}.".format(new_name), 0.005)
                    print('')
                    
                    retry = False
                    
                    while not retry:
                        print_by_char('Would you like to keep it the same? (y\\n): ', 0.005, False)
                        decision = input().lower()
                        if decision == "y" or decision == "yes":
                            return active_actions.pop(2), active_actions.pop(2) 
                        elif decision == "n" or decision == "no":
                            print('')
                            retry = True
                            break
                        else:
                            print('')
                            print_by_char('> Please answer yes or no.', 0.005)
                            print('')
                    
                    if retry:
                        continue
                        
                for file in os.listdir(saves_dir):
                    if file.endswith(".dat"):
                        if new_name + ".dat" == file:
                            name_taken = True
                            print('')
                            print_by_char("> This name is already taken.", 0.005)
                            print('')
                            break
                if len(new_name) < 20 and not name_taken:
                    name_set = True
                elif len(new_name) > 20:
                    print('')
                    print_by_char('> Max amount of characters: 20', 0.005)
                    print_by_char('> Try again..', 0.005)
                    print('')
                    
            os.remove(saves_dir + current_name + '.dat')
            player.set_name(new_name)
            save_game(player, map_objects, saves_dir, False)            
            print_by_char('\n> Name changed to {}.'.format(new_name), 0.005)
            return active_actions.pop(2), active_actions.pop(2)
        else:
            print_by_char('change what?', 0.005)
    else:
        print_by_char('change what?', 0.005)
        

def save_before_quit(player, map_objects, saves_dir):
    
    while True:
        print_by_char('Would you like to save before quitting? (y\\n): ', 0.005, False)
        decision = input().lower()
        
        if decision == "y" or decision == "yes":
            print('')
            save_game(player, map_objects, saves_dir)
            break
        
        elif decision == "n" or decision == "no":
            break
        
        else:
            print('')
            print_by_char('Please answer yes or no.', 0.005)
            print('')
    


def debug_command(raw_parts, raw_word_count, fixed_parts, fixed_word_count, active_actions, num_actv_actions, active_arts, active_locs, active_objs):
    print('')
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
    print('')
    

def debug_action(active_actions, has_article, has_adj, has_sec_adj, has_dir_obj, has_prep, has_prep_art, has_prep_adj, has_sec_prep_adj, has_prep_obj):
    print('')
    print('DEBUGGING PER ACTION({} at {}):'.format(active_actions[0], active_actions[1]))
    print('Has article: {}'.format(has_article[0]))
    print('Has adjective: {}'.format(has_adj[0]))
    print('Has second adjective: {}'.format(has_sec_adj[0]))
    print('Has direct object: {}'.format(has_dir_obj[0]))
    print('Has preposition: {}'.format(has_prep[0]))
    print('Has preposition article: {}'.format(has_prep_art[0]))
    print('Has preposition adjective: {}'.format(has_prep_adj[0]))
    print('Has second preposition adjective: {}'.format(has_sec_prep_adj[0]))
    print('Has object of preposition: {}'.format(has_prep_obj[0])) 
    print('')
