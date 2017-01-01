'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import sys, time, pickle, os
import random

def intro():
    time.sleep(1)
    print_by_char('------------------------------------------', 0.01)
    time.sleep(1)
    sys.stdout.write('                ')
    print_by_char('7 Stories', 0.05)
    time.sleep(1)
    print_by_char("A Hacker's Ambition to Destroy the Internet", 0.05)
    time.sleep(1)
    print_by_char('------------------------------------------', 0.01)
    

def print_by_char(text, sec, newline=True):
    if newline:
        text = text + '\n' 
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sec)
        

def load_option(saves_dir):
    
    while True:
        #WINDOWS: cwd = os.getcwd() + "\saves\\"
        #LINUX: cwd = os.getcwd() + "/saves/"
        save_exists = False
        
        char_names = []
        char_dict = {}
        
        counter = 1
        for file in os.listdir(saves_dir):
            if file.endswith(".dat"):
                save_exists = True
                
                #with open(cwd + '\\' + file, 'rb') as f:
                with open(saves_dir + file, 'rb') as f:
                    hero, map_objects, item_objects = pickle.load(f)
                    char_names.append(hero.get_name())
                    char_dict[str(counter)] = hero.get_name()
                    counter += 1
        
        if not save_exists:
            return create_char(saves_dir)
    
    
        print_by_char("Your Characters:", 0.01)
            
        for num in range(len(char_names)):
            print_by_char(">> "+ str(num + 1) + ": " + char_names[num], 0.01)
                
                
        print_by_char('------------------------------------------', 0.01)
        print_by_char('Enter character number or use "new" to', 0.01)
        print_by_char('create a new one.  To remove a character,', 0.01)
        print_by_char('use "delete #" with the number of the', 0.01)
        print_by_char('character you want to delete.', 0.01)
            
        while True:    
            #print_by_char('------------------------------------------', 0.01)
            print('------------------------------------------')
            print_by_char('Character: ', 0.01, False)
            decision = input().lower()
            
            parts = decision.split()
            
            chars_modified = False
            
            for part in parts:
                if part == "delete" or part == "remove" or part == "erase":
                    if len(parts) > parts.index(part) + 1:
                        if parts[parts.index(part) + 1] in char_dict:
                            print('------------------------------------------')
                            if part == "delete":
                                print_by_char('Deleted ' + char_dict[parts[parts.index(part) + 1]] + ".", 0.01)
                            elif part == "remove":
                                print_by_char('Removed ' + char_dict[parts[parts.index(part) + 1]] + ".", 0.01)
                            else:
                                print_by_char('Erased ' + char_dict[parts[parts.index(part) + 1]] + ".", 0.01)
                            remove_char(char_dict[parts[parts.index(part) + 1]], saves_dir)
                            char_names.remove(char_dict[parts[parts.index(part) + 1]])
                            del char_dict[parts[parts.index(part) + 1]]
                            chars_modified = True
                            print('------------------------------------------')
                            break
                        else:
                            print('------------------------------------------')
                            print_by_char('You must provide a character to ' + part + '.', 0.01)
                            break
                    else:
                        print('------------------------------------------')
                        print_by_char('You must provide a character to ' + part + '.', 0.01)
                        break
                elif part == "new":
                    return create_char(saves_dir)
                elif part in char_dict:
                    print('------------------------------------------')
                    print_by_char('Loaded ' + char_dict[part] + '.', 0.01)
                    return char_dict[part]
                else:
                    print('------------------------------------------')
                    print_by_char('Invalid command!', 0.01)
                    break
                
            if not parts:
                print_by_char('>>> You must enter something!', 0.01)
                
            if chars_modified == True:
                break
    
    
def remove_char(char, saves_dir):
    return os.remove(saves_dir + char + '.dat')


def create_char(saves_dir):
    name_set = False
    
    while name_set is False:
        print('------------------------------------------')
        name = input('Enter your name: ')
        
        for file in os.listdir(saves_dir):
            if file.endswith(".dat"):
                if name + ".dat" == file:
                    print("This name is already taken")
                    break
        
        if len(name) > 20:
            print('------------------------------------------')
            print('Max amount of characters: 20')
            print('Try again..')
        else:
            name_set = True
        
        
    init_char(name, saves_dir)        
    return name
    

def init_char(name, saves_dir):
    from game_objects import Player, Lab, Dorm, Room, Club, Phone
    # Creating main player
    player = Player(name)
    
    map_objects = {'lab': Lab(), 'dorm': Dorm(), 'room': Room(), 'club': Club()}
    
    item_objects = {'phone' : Phone()}
    
    with open(saves_dir + name + '.dat', 'wb') as f:
        pickle.dump([player, map_objects, item_objects], f, protocol=4)

    
def save_game(player, map_objects, item_objects, saves_dir):
    
    with open(saves_dir + player.get_name() + '.dat', 'wb') as f:
        pickle.dump([player, map_objects, item_objects], f, protocol=4)
        
    print_by_char('Saved ' + player.get_name() + '.', 0.01)
            