import sys
sys.path.append('../src')
import YearData as year_data
from YearData import YearData
from MockUuid import MockUuid
from testUtils import assertThatRaisedBy

mockUuid = MockUuid()

year_data.uuid = mockUuid

def testGetYear():
    yearData = YearData(2023)
    assert yearData.getYear() == 2023
testGetYear()

def testToJson():
    yearData = YearData(2023)
    assert yearData.toJson() == """{
    "year": 2023,
    "tags": []
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
    ]
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
    "tags": []
}"""
    assertThatRaisedBy(lambda: yearData.fromJson(jsonString), 'Invalid year. Expected 2023 but the file contains 2022.')
testFromJsonRaisesErrorWhenYearIsWrong()


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
    ]
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

