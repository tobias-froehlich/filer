import uuid
import json
import const
from datetime import date, datetime, timezone

class YearData:

    def __init__(self, year):
        self.__data = {
            'year': year,
            'tags': [],
            'documents': [],
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

    def getNextDocumentId(self):
        result = 0
        for document in self.__documents:
            if document['id'] > result:
                result = document['id']
        return result + 1

    def addDocument(self, description, datedAt, tagIds):
        try:
           parsedDate = date.fromisoformat(datedAt)
        except:
           raise Exception(f'Invalid date "{datedAt}".')
        if parsedDate.year != self.__data['year']:
            raise Exception(f'The document dated at year {parsedDate.year} cannot be filed in year {self.__data["year"]}.')
        documentId = len(self.__data['documents']) + 1
        document = {
            'id': documentId,
            'description': description,
            'datedAt': datedAt,
            'filedAt': datetime.now(timezone.utc).isoformat(),
            'modifiedAt': None,
            'tags': tagIds,
        }
        self.__data['documents'].append(document)
        

    def getDocument(self, documentId):
        for document in self.__data['documents']:
            if document['id'] == documentId:
                return document
        raise Exception(f'Document with ID {documentId}  does not exist.')

    def toJson(self):
        return json.dumps(self.__data, indent=4)

    def fromJson(self, jsonString):
        object = json.loads(jsonString)
        if list(object.keys()) != list(self.__data.keys()):
            raise Exception('Invalid file content with keys ' + str(list(object.keys())) + '.')
        if object['year'] != self.__data['year']:
            raise Exception('Invalid year. Expected ' + str(self.__data['year']) + ' but the file contains ' + str(object['year']) + '.')
        maxDocumentId = len(object['documents'])
        documentIds = []
        for document in object['documents']:
            documentIds.append(document['id'])
        for i in range(1, maxDocumentId + 1):
            if i not in documentIds:
                raise Exception(f'Document ID {i} is missing.')
        self.__data = object

        
