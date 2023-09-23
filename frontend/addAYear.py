import os

def addAYear(backend):
    
    quit = False
    
    menu = \
    """
        <number>: add a year
        quit:     quit
    """
    
    os.system('clear')
    while not quit:
        print(menu)
        i = input()
        os.system('clear')    
        if i.isdigit():
            try:
               backend.addYear(int(i))
               backend.save(int(i))
               quit = True
            except Exception as e:
                print(e)
        elif i == 'quit':
            quit = True
        else:
            print('Invalid input')
    
