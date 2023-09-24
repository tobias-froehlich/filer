import sys
sys.path.append('../src')
import YearData as year_data
from YearData import YearData
from MockUuid import MockUuid
from MockDatetime import MockDatetime
from testUtils import assertThatRaisedBy
from datetime import datetime, timezone

mockUuid = MockUuid()
year_data.uuid = mockUuid

mockDatetime = MockDatetime()
year_data.datetime = mockDatetime

def testGetYear():
    yearData = YearData(2023)
    assert yearData.getYear() == 2023
testGetYear()

def testToJson():
    yearData = YearData(2023)
    assert yearData.toJson() == """{
    "year": 2023,
    "tags": [],
    "documents": []
}"""
testToJson()

def testFromJson():
    yearData = YearData(2023)
    jsonString = """{
    "year": 2023,
    "tags": [
        {
            "id": "111",
            "name": "Tag 1"
        },
        {
            "id": "222",
            "name": "Tag 2"
        }
    ],
    "documents": []
}"""
    yearData.fromJson(jsonString)
    assert yearData.getYear() == 2023
    assert yearData.getTagIds() == ["111", "222"]
    assert yearData.getTagName("111") == "Tag 1"
    assert yearData.getTagName("222") == "Tag 2"
testFromJson()

def testFromJsonRaisesErrorWhenKeyIsMissing():
    yearData = YearData(2023)
    jsonString = """{
    "tags": []
}"""
    assertThatRaisedBy(lambda: yearData.fromJson(jsonString), 'Invalid file content with keys [\'tags\'].')
testFromJsonRaisesErrorWhenKeyIsMissing()

def testFromJsonRaisesErrorWhenInvalidKeyExists():
    yearData = YearData(2023)
    jsonString = """{
    "year": 2023,
    "tags": [],
    "uselessKey": null
}"""
    assertThatRaisedBy(lambda: yearData.fromJson(jsonString), 'Invalid file content with keys [\'year\', \'tags\', \'uselessKey\'].')
testFromJsonRaisesErrorWhenInvalidKeyExists()

def testFromJsonRaisesErrorWhenYearIsWrong():
    yearData = YearData(2023)
    jsonString = """{
    "year": 2022,
    "tags": [],
    "documents": []
}"""
    assertThatRaisedBy(lambda: yearData.fromJson(jsonString), 'Invalid year. Expected 2023 but the file contains 2022.')
testFromJsonRaisesErrorWhenYearIsWrong()


def testFromJsonRaisesErrorWhenDocumentIdIsMissing():
    yearData = YearData(2023)
    jsonString = """{
    "year": 2023,
    "tags": [],
    "documents": [
        {
            "id": 1,
            "description": "description 1",
            "datedAt": "2023-09-24",
            "filedAt": "2023-09-25T14:17:00.000Z",
            "tags": []
        },
        {
            "id": 3,
            "description": "description 3",
            "datedAt": "2023-09-23",
            "filedAt": "2023-09-24T10:05:00.000Z",
            "tags": []
        }
    ]
}"""
    assertThatRaisedBy(lambda: yearData.fromJson(jsonString), 'Document ID 2 is missing.')
testFromJsonRaisesErrorWhenDocumentIdIsMissing()



def testAddTag():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    yearData.addTag('My Tag')
    assert yearData.toJson() == """{
    "year": 2023,
    "tags": [
        {
            "id": "111",
            "name": "My Tag"
        }
    ],
    "documents": []
}"""
    mockUuid.assertThatAllUuidsWereUsed()
testAddTag()

def testTagNameAlreadyExists():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    assertThatRaisedBy(lambda: yearData.addTag('Tag 1'), 'Tag name already exists.')
    mockUuid.assertThatAllUuidsWereUsed()
testTagNameAlreadyExists()   


def testUuidCollision():
    mockUuid.reset()
    mockUuid.add('111')
    mockUuid.add('111')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    assertThatRaisedBy(lambda: yearData.addTag('Tag 2'), 'The id already exists.')
    mockUuid.assertThatAllUuidsWereUsed()
testUuidCollision()   

def testTooShortTagName():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    assertThatRaisedBy(lambda: yearData.addTag('abc'), 'Tag name is too short.')
    mockUuid.assertThatAllUuidsWereUsed()
testTooShortTagName()

def testTooLongTagName():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    assertThatRaisedBy(lambda: yearData.addTag('abcdefghijklmnopq'), 'Tag name is too long.')
    mockUuid.assertThatAllUuidsWereUsed()
testTooLongTagName()

def testAddTagWithId():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    yearData.addTag('Tag 2', '222')
    assert yearData.getTagIds() == ['111', '222']
    assert yearData.getTagName('222') == 'Tag 2'
    mockUuid.assertThatAllUuidsWereUsed()
testAddTagWithId()

def testAddTagWithExistingId():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    assertThatRaisedBy(lambda: yearData.addTag('Tag 2', '111'), 'The id already exists.')
    mockUuid.assertThatAllUuidsWereUsed()
testAddTagWithExistingId()

def testAddTagWithExistingName():
    mockUuid.reset()
    mockUuid.add('111')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    assertThatRaisedBy(lambda: yearData.addTag('Tag 1', '222'), 'Tag name already exists.')
    mockUuid.assertThatAllUuidsWereUsed()
testAddTagWithExistingName()

def testGetTagName():
    mockUuid.reset()
    mockUuid.add('111')
    mockUuid.add('222')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    yearData.addTag('Tag 2')
    assert yearData.getTagName('111') == 'Tag 1'
    mockUuid.assertThatAllUuidsWereUsed()
testGetTagName()

def testGetTagIds():
    mockUuid.reset()
    mockUuid.add('111')
    mockUuid.add('222')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    yearData.addTag('Tag 2')
    assert yearData.getTagIds() == ['111', '222']
    mockUuid.assertThatAllUuidsWereUsed()
testGetTagIds()

def testGetTagNameRaisesError():
    mockUuid.reset()
    mockUuid.add('111')
    mockUuid.add('222')
    yearData = YearData(2023)
    yearData.addTag('Tag 1')
    yearData.addTag('Tag 2')
    assertThatRaisedBy(lambda: yearData.getTagName('333'), 'Could not find tag.')
    mockUuid.assertThatAllUuidsWereUsed()
testGetTagNameRaisesError()


def testAddDocument():
    mockDatetime.reset()
    mockDatetime.add(datetime(
        2023, 9, 24, 13, 9, 29, 799976,
        tzinfo=timezone.utc
    ))
    yearData = YearData(2023)
    yearData.addDocument('my description', '2023-09-23', [])
    assert yearData.getDocument(1)['description'] == 'my description'
    assert yearData.getDocument(1)['datedAt'] == '2023-09-23'
    assert yearData.getDocument(1)['filedAt'] == '2023-09-24T13:09:29.799976+00:00'
    assert yearData.getDocument(1)['modifiedAt'] == None
    assert yearData.getDocument(1)['tags'] == []
testAddDocument()

def testRaiseErrorIfDatedAtIsNotValid():
    mockDatetime.reset()
    mockDatetime.add(datetime(
        2023, 9, 24, 13, 9, 29, 799976,
        tzinfo=timezone.utc
    ))
    yearData = YearData(2023)
    assertThatRaisedBy(lambda: yearData.addDocument('my description', '2023-09-31', []), 'Invalid date "2023-09-31".')
testRaiseErrorIfDatedAtIsNotValid()

def testRaiseErrorIfDatedAtIsWrongYear():
    mockDatetime.reset()
    mockDatetime.add(datetime(
        2023, 9, 24, 13, 9, 29, 799976,
        tzinfo=timezone.utc
    ))
    yearData = YearData(2023)
    assertThatRaisedBy(lambda: yearData.addDocument('my description', '2024-09-29', []), 'The document dated at year 2024 cannot be filed in year 2023.')
testRaiseErrorIfDatedAtIsWrongYear()

def testAddDocumentsWithTags():
    mockDatetime.reset()
    mockDatetime.add(datetime(
        2023, 9, 24, 13, 9, 29, 799976,
        tzinfo=timezone.utc
    ))
    mockDatetime.add(datetime(
        2023, 9, 24, 13, 12, 20, 30079,
        tzinfo=timezone.utc
    ))
    yearData = YearData(2023)
    yearData.addTag('tag-id-1', 'my tag')
    yearData.addTag('tag-id-2', 'your tag')
    yearData.addTag('tag-id-3', 'other tag')
    yearData.addDocument(
        'the description 1',
        '2023-09-24',
        ['tag-id-1', 'tag-id-3']
    )
    yearData.addDocument(
        'the description 2',
        '2023-09-24',
        ['tag-id-3']
    )
    assert yearData.getDocument(1)['description'] == 'the description 1'
    assert len(yearData.getDocument(1)['tags']) == 2
    assert yearData.getDocument(1)['tags'][0] == 'tag-id-1'
    assert yearData.getDocument(1)['tags'][1] == 'tag-id-3'
    assert yearData.getDocument(2)['description'] == 'the description 2'
    assert len(yearData.getDocument(2)['tags']) == 1
    assert yearData.getDocument(2)['tags'][0] == 'tag-id-3'
testAddDocumentsWithTags()

