import os
import sys
import json
sys.path.append('../backend/src/')
from Backend import Backend
from addAYear import addAYear
from chooseAYear import chooseAYear
from showTags import showTags
from addATag import addATag

def frontend():
    if not os.path.isfile(os.path.expanduser('~/filer.conf')):
       raise Exception("""
The file ~/filer.conf is missing. It must contain for example the following content:
{
    "filer_directory": "~/filer_example/"
}
""")
    with open(os.path.expanduser('~/filer.conf'), 'r') as f:
        conf = json.loads(f.read())
    print(conf)
    backend = Backend(os.path.expanduser(conf['filer_directory']))

    quit = False
   
    activeYear = None
 
    def getMenu():
        if activeYear:
            return """
        a:    choose year {latestYear}
        b:    choose a year
        c:    add a year
        d:    show tags
        e:    add a tag
        quit: quit
    """.format(latestYear = max(backend.getYears()))
        else:
            return """
        a:    choose year {latestYear}
        b:    choose a year
        c:    add a year
        quit: quit
    """.format(latestYear = max(backend.getYears()))
   
    os.system('clear')
    while not quit:
        if activeYear:
            print('Year: {year}'.format(year = activeYear))
        print(getMenu())
        i = input()
        if i == 'a':
            activeYear = max(backend.getYears())
            os.system('clear')
        elif i == 'b':
            activeYear = chooseAYear(backend)
            os.system('clear')
        elif i == 'c':
            addAYear(backend)
        elif activeYear and i == 'd':
            os.system('clear')
            showTags(backend, activeYear)
        elif activeYear and i == 'e':
            os.system('clear')
            addATag(backend, activeYear)
        elif i == 'quit':
            quit = True
        else:
            os.system('clear')
            print('Invalid input hello')

frontend() 
