'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import sys, time, pickle, os
import random
import getpass

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
    
    
def display_level(level):
    if level == 1:
        sys.stdout.write('            ')
        print_by_char('Level 1 : ', 0.01, False)
        time.sleep(0.5)
        print_by_char('Facebook', 0.01, False)
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
    for i in range(len(loc_obj.current_prompt)):
        for line in loc_obj.current_prompt[i]:
            print_by_char(line, 0.01)
        
        if i < len(loc_obj.current_prompt) - 1:
            print('')
        
    
    loc_obj.get_current_prompt(loc_obj.first_visit, loc_obj.current_prompt, player)
    

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
                    print('------------------------------------------')
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
    print_dots(3)
    time.sleep(0.5)
    print_by_char(' and like that.', 0.01)
    time.sleep(1)
    
    print("")
    
    print_by_char('You spawn in outside the massive doors of', 0.01)
    print_by_char('the Internet, a giant tower planted on a', 0.01)
    print_by_char('floating rock in the night sky.  With no', 0.01)
    print_by_char('direction, you pull out a laptop and power', 0.01)
    print_by_char('it on.  The screen prompts you', 0.01, False)
    print_dots(2)
    print('\n------------------------------------------')
    print_by_char('"You must create an account before you can', 0.01)
    print_by_char('use the computer.', 0.01)
    
    print("")
    
    name_set = False
    password_set = False
    
    while name_set is False:
        name_taken = False
        print_by_char('Create a username: ', 0.01, False)
        name = input()
        
        for file in os.listdir(saves_dir):
            if file.endswith(".dat"):
                if name + ".dat" == file:
                    name_taken = True
                    print('')
                    print_by_char("> This name is already taken.", 0.01)
                    print('')
                    break
        
        if len(name) < 20 and not name_taken:
            name_set = True
        elif len(name) > 20:
            print('')
            print_by_char('> Max amount of characters: 20', 0.01)
            print_by_char('> Try again..', 0.01)
            print('')
    
    while password_set is False:
        print_by_char('Create a password: ', 0.01, False)
        password = input()
        pass_chars = []
        for char in password: pass_chars.append(char)
        
        if password == 'quit':
            print('')
            print_by_char('> You cannot use that as a password!', 0.01)
            print('')
            continue
        elif ' ' in pass_chars:
            print('')
            print_by_char('> You cannot include a space!', 0.01)
            print('')
            continue
        
        print_by_char('Re-enter password: ', 0.01, False)
        retype = input()
        
        if password == retype:
            password_set = True
        else:
            print('')
            print_by_char('> Passwords do not match!', 0.01)
            print('')
        
    print_by_char('Password hint: ', 0.01, False)
    pass_hint = input()
    
    
    print("")
    print_dots(3)
    print_by_char(' Account created successfully."', 0.01)
    init_char(name, password, pass_hint, saves_dir)
    
    print('------------------------------------------')
    print_by_char('Your fate lies ahead.  Many things are', 0.01)
    print_by_char('about to happen, so try your hardest to', 0.01)
    print_by_char("pay attention.  Just don't forget that the", 0.01)
    print_by_char('bottom is the key and the top is the goal.', 0.01)
    print('------------------------------------------')
    print_by_char("Press 'enter' to start your journey", 0.01, False)
    print_dots(2)
    getpass.getpass("")
    
    return name
    

def init_char(name, password, pass_hint, saves_dir):
    from game_objects import Player, Laptop, Front_lobby, South_Hall
    # Creating main player
    player = Player(name)
    
    map_objects = {'Front Lobby': Front_lobby(), 'South Hall': South_Hall()}
    
    item_objects = {'laptop' : Laptop(name, password, pass_hint)}
    
    with open(saves_dir + name + '.dat', 'wb') as f:
        pickle.dump([player, map_objects, item_objects], f, protocol=4)

    
def save_game(player, map_objects, item_objects, saves_dir):
    
    with open(saves_dir + player.get_name() + '.dat', 'wb') as f:
        pickle.dump([player, map_objects, item_objects], f, protocol=4)
        
    print_by_char('Saved ' + player.get_name() + '.', 0.01)
    
    
def print_dots(count, newline=False):
    for i in range(0, count):
        print_by_char('.', 0.01, False)
        time.sleep(0.5)
    
    if newline:
        print("\n")
            