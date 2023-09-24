import sys
sys.path.append('../src')
import os
import shutil
import YearData as year_data
from YearData import YearData
from Backend import Backend
from MockUuid import MockUuid
from testUtils import assertThatRaisedBy

mockUuid = MockUuid()
year_data.uuid = mockUuid

def clean():
    if 'filertest' in os.listdir('/tmp/'):
        for filename in os.listdir('/tmp/filertest/'):
            os.remove(os.path.join('/tmp/filertest', filename))
        os.rmdir('/tmp/filertest')
    os.mkdir('/tmp/filertest')

def testLoadDataWhenDirectoryIsEmpty():
    clean()
    backend = Backend('/tmp/filertest')
    assert len(backend.getYears()) == 0
testLoadDataWhenDirectoryIsEmpty()

def testLoadDataRaisesErrorWhenFileHasWrongEnding():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/2023.pdf')
    assertThatRaisedBy(lambda: Backend('/tmp/filertest'), 'Unknown file ending in file "2023.pdf".')
testLoadDataRaisesErrorWhenFileHasWrongEnding()

def testLoadDataRaisesErrorWhenFileNameIsNotAYear():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/20a23.txt')
    assertThatRaisedBy(lambda: Backend('/tmp/filertest'), 'File name "20a23.txt" is not a year.')
testLoadDataRaisesErrorWhenFileHasWrongEnding()

def testLoadDataWhenDirectoryHasOneFile():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/2023.txt')
    backend = Backend('/tmp/filertest')
    assert len(backend.getYears()) == 1
    assertThatRaisedBy(lambda: backend.getYearData(2024), 'Year 2024 does not exist.')
    assert backend.getYearData(2023).getYear() == 2023
    assert backend.getYearData(2023).getTagIds() == ['eb69474c-ce4f-44e7-a8c6-c314c50521c0', '6bb5dd6a-923a-4714-9255-fb0bcc0a10ac']
    assert backend.getYearData(2023).getTagName('eb69474c-ce4f-44e7-a8c6-c314c50521c0') == 'Tag 1'
    assert backend.getYearData(2023).getTagName('6bb5dd6a-923a-4714-9255-fb0bcc0a10ac') == 'Tag 2'
testLoadDataWhenDirectoryHasOneFile()

def loadDataWhenYearHasNoTags():
    clean()
    shutil.copy('testfiles/2023_noTags.txt', '/tmp/filertest/2023.txt')
    backend = Backend('/tmp/filertest') 
loadDataWhenYearHasNoTags()

def testValidationWhenYearsHaveTagsWithSameIdButDifferentName():
    clean()
    shutil.copy('testfiles/tagsWithSameIdButDifferentName/2022.txt', '/tmp/filertest/2022.txt')
    shutil.copy('testfiles/tagsWithSameIdButDifferentName/2023.txt', '/tmp/filertest/2023.txt')
    assertThatRaisedBy(lambda: Backend('/tmp/filertest'), 'Tags "Tag 3" of year 2023 and "Tag 2" of year 2022 have the same ID.')

testValidationWhenYearsHaveTagsWithSameIdButDifferentName()
    
def testValidationWhenYearsHaveTagsWithSameNameButDifferentIds():
    clean()
    shutil.copy('testfiles/tagsWithSameNameButDifferentIds/2022.txt', '/tmp/filertest/2022.txt')
    shutil.copy('testfiles/tagsWithSameNameButDifferentIds/2023.txt', '/tmp/filertest/2023.txt')
    assertThatRaisedBy(lambda: Backend('/tmp/filertest'), 'Tags "Tag 2" of year 2023 and "Tag 2" of year 2022 have the same name but different IDs.')

testValidationWhenYearsHaveTagsWithSameNameButDifferentIds()

def testAddYearThatAlreadyExists():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/2023.txt')
    backend = Backend('/tmp/filertest')
    assertThatRaisedBy(lambda: backend.addYear(2023), 'Year 2023 already exists.')
testAddYearThatAlreadyExists()

def testAddYear():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/2023.txt')
    backend = Backend('/tmp/filertest')
    backend.addYear(2024)
    assert backend.getYears() == [2023, 2024]
testAddYear()

def testSaveYearThatDoesNotExist():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/2023.txt')
    backend = Backend('/tmp/filertest')
    assertThatRaisedBy(lambda: backend.save(2024), 'Year 2024 does not exist.') 
testSaveYearThatDoesNotExist()

def testSaveYear():
    clean()
    shutil.copy('testfiles/2023.txt', '/tmp/filertest/2023.txt')
    backend = Backend('/tmp/filertest')
    backend.addYear(2024)
    backend.save(2024)
    with open('/tmp/filertest/2024.txt', 'r') as f:
        data = f.read()
    assert data == """{
    "year": 2024,
    "tags": [],
    "documents": []
}"""
testSaveYear()
