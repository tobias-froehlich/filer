import os

def addANewTag(backend, activeYear):
    
    quit = False
    
    menu = \
    """
        <something>: tag name
        quit:        quit
    """
    
    os.system('clear')
    while not quit:
        print(menu)
        i = input()
        os.system('clear')    
        if i == 'quit':
            quit = True
        else:
            try:
               backend.getYearData(activeYear).addTag(i)
               backend.save(activeYear)
               quit = True
            except Exception as e:
                print(e)
    
