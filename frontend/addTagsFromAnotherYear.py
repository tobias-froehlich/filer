import os
from chooseAYear import chooseAYear

def addTagsFromAnotherYear(backend, activeYear): 
    otherYear = chooseAYear(backend)

    if otherYear == None:
        return

    quit = False
   

    tagIds = backend.getYearData(otherYear).getTagIds()
    tagNames = [backend.getYearData(otherYear).getTagName(id) for id in tagIds]
    tagSelected = []
    for tagId in tagIds:
        if tagId in backend.getYearData(activeYear).getTagIds():
           tagSelected.append(True)
        else:
           tagSelected.append(False)

    def getCheckbox(value):
        if value:
            return '[x]'
        else:
            return '[ ]'


    def getMenu():
        liste = ''
        i = 1
        for tagName in tagNames:
            liste += f'    {i} {getCheckbox(tagSelected[i - 1])}: {tagName}\n'
            i += 1

        if len(tagIds) > 0:
            menu = \
            """
Choose a tag from the year {otherYear} and add it to the year {activeYear}:
{liste}        
        quit:        quit
            """.format(otherYear = otherYear, activeYear = activeYear, liste = liste)
        else:
            menu = \
            """
No tags in year {otherYear}        
        quit:        quit
            """.format(otherYear = otherYear)
        return menu
 
    
    os.system('clear')
    while not quit:
        print(getMenu())
        i = input()
        os.system('clear')    
        if i == 'quit':
            quit = True
        elif i.isdigit() and int(i) > 0 and int(i) <= len(tagIds) and not tagSelected[int(i) - 1]:
            try:
               backend.getYearData(activeYear).addTag(tagNames[int(i) - 1], tagIds[int(i) - 1])
               backend.save(activeYear)
               tagSelected[int(i) - 1] = True
               os.system('clear') 
            except Exception as e:
                print(e)
        else:
            print('Invalid input')
    
