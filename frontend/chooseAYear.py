import os

def chooseAYear(backend):
    
    quit = False
    
    menu = \
    """
        <number>: choose a year
        a:        show available years
        quit:     quit
    """
    
    os.system('clear')
    while not quit:
        print(menu)
        i = input()
        if i.isdigit():
            if int(i) in backend.getYears():
               return int(i)
            else:
                os.system('clear')    
                print('Invalid input')
        elif i == 'a':
            os.system('clear')    
            for year in backend.getYears():
                print(year)
        elif i == 'quit':
            quit = True
        else:
            print('Invalid input')
    
