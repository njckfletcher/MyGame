'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import sys, time, pickle, os

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

def loadin(file):
    with open(file, 'rb') as f:
        hero, map_objects, item_objects = pickle.load(f) 
        

def load_option():
    
    cwd = os.getcwd() + "\saves"
    
    save_exists = False
    
    char_names = []
    
    for file in os.listdir(cwd):
        if file.endswith(".dat"):
            save_exists = True
            
            with open(cwd + '\\' + file, 'rb') as f:
                hero, map_objects, item_objects = pickle.load(f)
                #hero = pickle.load(f)
                char_names.append(hero.get_name())
    
    if not save_exists:
        create_char()
    
    print_by_char("Your Characters:", 0.01, True)
    
    for num in range(len(char_names)):
        print_by_char(">> "+ str(num + 1) + ": " + char_names[num], 0.01, True)
    

def create_char():
    cwd = os.getcwd() + "\saves"
    name_set = False
    
    while name_set is False:
        print('------------------------------------------')
        name = input('Enter your name: ')
        
        for file in os.listdir(cwd):
            if file.endswith(".dat"):
                if name + ".dat" == file:
                    print("This name is already taken")
                    continue
        
        if len(name) > 20:
            print('------------------------------------------')
            print('Max amount of characters: 20')
            print('Try again..')
        else:
            name_set = True
            
        return name
    
    
def save_game(player, map_objects, item_objects):
    
    with open(player.get_name + '.dat', 'wb') as f:
        pickle.dump([player, map_objects, item_objects], f, protocol=4)
            