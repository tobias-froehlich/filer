import os
from chooseAYear import chooseAYear

def addATagFromAnotherYear(backend, activeYear):
    
    otherYear = chooseAYear(backend)

    if otherYear == None:
        return

    quit = False
   

    tagIds = backend.getYearData(otherYear).getTagIds()
    tagNames = [backend.getYearData(otherYear).getTagName(id) for id in tagIds]

    liste = ''
    i = 1
    for tagName in tagNames:
        liste += '    {i}: {name}\n'.format(i = i, name = tagName)
        i += 1

    if len(tagNames) > 0: 
        menu = \
        """
    Choose a tag from the year {otherYear} and add it to the year {activeYear}:
{liste}        
            quit:        quit
        """.format(otherYear = otherYear, activeYear = activeYear, liste = liste)
    else:
        menu = \
        f"""
    The year {otherYear} has no tags.
            quit: quit
        """
    
    os.system('clear')
    while not quit:
        print(menu)
        i = input()
        os.system('clear')    
        if i == 'quit':
            quit = True
        elif i.isdigit() and int(i) > 0 and int(i) <= len(tagIds):
            try:
               backend.getYearData(activeYear).addTag(tagNames[int(i) - 1], tagIds[int(i) - 1])
               backend.save(activeYear)
               os.system('clear')
               print('Tag \'{tagName}\' added to year {year}'.format(tagName = tagNames[int(i) - 1], year = activeYear))
               quit = True
            except Exception as e:
                print(e)
        else:
            print('Invalid input')
    
