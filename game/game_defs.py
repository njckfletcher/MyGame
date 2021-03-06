'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import sys, time, pickle, os
import random
import getpass

def intro():
    time.sleep(1)
    print_by_char('--------------------------------------------', 0.005)
    time.sleep(1)
    sys.stdout.write('                ')
    print_by_char('7 Stories', 0.05)
    time.sleep(1)
    print_by_char("A Hacker's Ambition to Destroy the Internet", 0.05)
    time.sleep(1)
    print_by_char('--------------------------------------------', 0.005)
    
    
def display_level(level):
    if level == 1:
        sys.stdout.write('            ')
        print_by_char('Level 1 : ', 0.005, False)
        time.sleep(0.5)
        print_by_char('Facebook', 0.005, False)
        time.sleep(0.5)
    if level == 2:
        pass
    if level == 3:
        pass
    if level == 4:
        pass
    if level == 5:
        pass
    if level == 6:
        pass
    if level == 7:
        pass
    
    
def display_prompt(loc_obj, player):
    # Get current prompt
    
    
    for i in range(len(loc_obj.current_prompt)):
        for line in loc_obj.current_prompt[i]:
            print_by_char(line, 0.005)
        
        if i < len(loc_obj.current_prompt) - 1:
            print('')
            
    # Update current prompt
    loc_obj.update_current_prompt(loc_obj.first_visit, loc_obj.current_prompt, player)


def print_by_char(text, sec, newline=True):
    if newline:
        text = text + '\n' 
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sec)
        

def load_option(saves_dir):
    
    while True:
        save_exists = False
        
        char_names = []
        char_dict = {}
        
        counter = 1
        for file in os.listdir(saves_dir):
            if file.endswith(".dat"):
                save_exists = True
                
                with open(saves_dir + file, 'rb') as f:
                    hero, map_objects = pickle.load(f)
                    char_names.append(hero.get_name())
                    char_dict[str(counter)] = hero.get_name()
                    counter += 1
        
        if not save_exists:
            return create_char(saves_dir)
    
    
        print_by_char("Your Characters:", 0.005)
            
        for num in range(len(char_names)):
            print_by_char(">> "+ str(num + 1) + ": " + char_names[num], 0.005)
                
                
        print_by_char('--------------------------------------------', 0.005)
        print_by_char('Available options:', 0.005)
        print_by_char('> new', 0.005)
        print_by_char('> load [number]', 0.005)
        print_by_char('> reset [number]', 0.005)
        print_by_char('> delete, erase, remove [number]', 0.005)
            
        while True:    
            print('--------------------------------------------')
            print_by_char('Character: ', 0.005, False)
            decision = input().lower()
            
            parts = decision.split()
            
            chars_modified = False
            
            for part in parts:
                if part == "delete" or part == "remove" or part == "erase":
                    if len(parts) > parts.index(part) + 1:
                        if parts[parts.index(part) + 1] in char_dict:
                            char_name = char_dict[parts[parts.index(part) + 1]]
                            print('--------------------------------------------')
                            if part == "delete":
                                print_by_char('Deleted ' + char_name + '.', 0.005)
                            elif part == "remove":
                                print_by_char('Removed ' + char_name + '.', 0.005)
                            else:
                                print_by_char('Erased ' + char_name + '.', 0.005)
                            remove_char(char_name, saves_dir)
                            char_names.remove(char_name)
                            del char_dict[parts[parts.index(part) + 1]]
                            chars_modified = True
                            print('--------------------------------------------')
                            break
                        else:
                            print('--------------------------------------------')
                            print_by_char('You must provide a character to ' + part + '.', 0.005)
                            break
                    else:
                        print('--------------------------------------------')
                        print_by_char('You must provide a character to ' + part + '.', 0.005)
                        break
                elif part == 'reset':
                    if len(parts) > parts.index(part) + 1:
                        if parts[parts.index(part) + 1] in char_dict:
                            char_name = char_dict[parts[parts.index(part) + 1]]
                            print('--------------------------------------------')
                            print_by_char('Reset '  + char_name + '.', 0.005)
                            reset_char(char_name, saves_dir)
                            break
                        else:
                            print('--------------------------------------------')
                            print_by_char('You must provide a character to ' + part + '.', 0.005)
                            break
                    else:
                        print('--------------------------------------------')
                        print_by_char('You must provide a character to ' + part + '.', 0.005)
                        break
                            
                elif part == "new":
                    print('--------------------------------------------')
                    return create_char(saves_dir)
                elif part == 'load':
                    if len(parts) > parts.index(part) + 1:
                        if parts[parts.index(part) + 1] in char_dict:
                            char_name = char_dict[parts[parts.index(part) + 1]]
                            print('--------------------------------------------')
                            print_by_char('Loaded '  + char_name + '.', 0.005)
                            return char_dict[parts[parts.index(part) + 1]]
                        else:
                            print('--------------------------------------------')
                            print_by_char('You must provide a character to ' + part + '.', 0.005)
                            break
                    else:
                        print('--------------------------------------------')
                        print_by_char('You must provide a character to ' + part + '.', 0.005)
                        break
                    
                else:
                    print('--------------------------------------------')
                    print_by_char('Invalid command!', 0.005)
                    break
                
            if not parts:
                print_by_char('>>> You must enter something!', 0.005)
                
            if chars_modified == True:
                break
    
    
def remove_char(char, saves_dir):
    return os.remove(saves_dir + char + '.dat')


def create_char(saves_dir):
    name_set = False
    
    print_dots(3)
    time.sleep(0.5)
    print_by_char(' and like that.', 0.005)
    time.sleep(1)
    
    print("")
    
    print_by_char('You spawn in outside the massive doors of', 0.005)
    print_by_char('the Internet, a giant tower planted on a', 0.005)
    print_by_char('floating rock in the night sky.  A nearby', 0.005)
    print_by_char('robot approaches you.', 0.005)
    print('')
    print_by_char('Robot: Hello my brave and fellow creator.', 0.005)
    print_by_char('Welcome to the Internet.  Behind these', 0.005)
    print_by_char('walls are the deceitful ruins of what the', 0.005)
    print_by_char('Internet really bestows.  It has been said', 0.005)
    print_by_char('that one day, you would appear right here', 0.005)
    print_by_char('where you are standing to enter these doors', 0.005)
    print_by_char('and bring down this building.  I was', 0.005)
    print_by_char('assigned to wait outside these doors for', 0.005)
    print_by_char('your impending arrival so that I could help', 0.005)
    print_by_char('get your journey going.  For starters, I', 0.005)
    print_by_char('want you to take this', 0.005, False), print_dots(2, True)
    print_by_char('The robot handed you a laptop.', 0.005)
    print('')
    print_by_char("Robot: You'll need that along your way.", 0.005)
    print_by_char("Of course, it's useless if you can't figure", 0.005)
    print_by_char('out how to use it.. hehe..  Anyways, may I', 0.005)
    print_by_char("ask for the creator's name?", 0.005)
    print('')
    while not name_set:
        name_taken = False
        print_by_char('Your name: ', 0.005, False)
        name = input()
        
        for file in os.listdir(saves_dir):
            if file.endswith(".dat"):
                if name.lower() + ".dat" == file.lower():
                    name_taken = True
                    print('')
                    print_by_char("Robot: It appears as though someone with", 0.005)
                    print_by_char("that name has already entered", 0.005, False), print_dots(2, True)
                    break
        
        if len(name) < 20 and not name_taken:
            name_set = True
            
        elif len(name) > 20:
            print('')
            print_by_char("Robot: I can't save a name that is more than", 0.005)
            print_by_char('20 characters long', 0.005, False), print_dots(2, True)
            
    print('')
    print_by_char('Robot: {}, yes.  You may call me Bytes.'.format(name), 0.005)
    print_by_char('Your fate lies ahead.  Many things are', 0.005)
    print_by_char('about to happen, so try your hardest to pay', 0.005)
    print_by_char("attention.  Just don't forget that the", 0.005)
    print_by_char('bottom is the key and the top is the goal.', 0.005)
    print_by_char("I'm sure that we will meet again.  Now, go", 0.005)
    print_by_char('through the doors.', 0.005)
    
    init_char(name, saves_dir)
    
    print('--------------------------------------------')
    print_by_char("Press 'enter' to start your journey", 0.005, False)
    print_dots(2)
    getpass.getpass("")
    
    return name


def reset_char(name, saves_dir):
    for file in os.listdir(saves_dir):
        if file.endswith(".dat"):
            if name.lower() + ".dat" == file.lower():
                os.remove(saves_dir + name + '.dat')
    init_char(name, saves_dir)
    

def init_char(name, saves_dir):
    from game_objects import Player, Front_lobby, South_Hall
    # Creating main player
    player = Player(name)
    
    map_objects = {'Front Lobby': Front_lobby(), 'South Hall': South_Hall()}
    
    with open(saves_dir + name + '.dat', 'wb') as f:
        pickle.dump([player, map_objects], f, protocol=4)

    
def save_game(player, map_objects, saves_dir, echo=True):
    
    with open(saves_dir + player.get_name() + '.dat', 'wb') as f:
        pickle.dump([player, map_objects], f, protocol=4)
        
    if echo:
        print_by_char('Saved ' + player.get_name() + '.', 0.005)
    
    
def print_dots(count, newline=False):
    for i in range(0, count):
        print_by_char('.', 0.005, False)
        time.sleep(0.5)
    
    if newline:
        print("\n")
            