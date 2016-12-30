'''
Created on Dec 21, 2016

@author: Hunter Malm
'''
import sys, time, pickle

def intro():
    time.sleep(1)
    print_by_char('------------------------------------------', 0.01)
    time.sleep(1)
    sys.stdout.write('                ')
    print_by_char('7 Stories', 0.05)
    time.sleep(1)
    print_by_char("A Hacker's Ambition to Destroy the Internet", 0.05)
    
    

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