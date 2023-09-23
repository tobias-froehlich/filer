import uuid
import json
import const

class YearData:

    def __init__(self, year):
        self.__data = {
            'year': year,
            'tags': [],
        }
        
    def getYear(self):
        return self.__data['year']

    def addTag(self, tagName, id=None):
        for tag in self.__data['tags']:
            if tag['name'] == tagName:
                raise Exception('Tag name already exists.')
        if id == None:
            id = uuid.uuid4().__str__()
        for tag in self.__data['tags']:
            if tag['id'] == id:
                raise Exception('The id already exists.')
        if len(tagName) < const.minTagNameLength:
            raise Exception('Tag name is too short.')
        if len(tagName) > const.maxTagNameLength:
            raise Exception('Tag name is too long.')
        self.__data['tags'].append({
            'id': id,
            'name': tagName,
        }) 

    def getTagName(self, id):
        for tag in self.__data['tags']:
            if tag['id'] == id:
                return tag['name']
        raise Exception('Could not find tag.')

    def getTagIds(self):
        result = []
        for tag in self.__data['tags']:
            result.append(tag['id'])
        return result

    def toJson(self):
        return json.dumps(self.__data, indent=4)

    def fromJson(self, jsonString):
        object = json.loads(jsonString)
        if list(object.keys()) != list(self.__data.keys()):
            raise Exception('Invalid file content with keys ' + str(list(object.keys())) + '.')
        if object['year'] != self.__data['year']:
            raise Exception('Invalid year. Expected ' + str(self.__data['year']) + ' but the file contains ' + str(object['year']) + '.')
        self.__data = object

    
