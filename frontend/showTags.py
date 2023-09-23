import os

def showTags(backend, activeYear):
    if not activeYear:
        print('No year selected!')
    else:
        try:
            tagIds = backend.getYearData(activeYear).getTagIds()
            if len(tagIds) == 0:
                print('No Tags for the year {year}.'.format(year = activeYear))
            else:
                print('The year {year} has the following tags:'.format(year = activeYear))
                for tagId in tagIds:
                    print('    ', backend.getYearData(activeYear).getTagName(tagId))
        except Exception as e:
            print(e)
