import os
from addATagFromAnotherYear import addATagFromAnotherYear
from addANewTag import addANewTag

def addATag(backend, activeYear):
    
    quit = False
    
    menu = \
    """
        a:    add a tag from another year
        b:    add a new tag
        quit: quit
    """
    
    os.system('clear')
    while not quit:
        print(menu)
        i = input()
        os.system('clear')    
        if i == 'a':
           addATagFromAnotherYear(backend, activeYear)
           quit = True
        if i == 'b':
           addANewTag(backend, activeYear)
        elif i == 'quit':
            quit = True
        else:
            print('Invalid input')
    
