import os
from YearData import YearData

class Backend:

    def __init__(self, directory):
        self.__directory = directory
        self.load()

    def load(self):
        filenames = os.listdir(self.__directory)
        self.__yearDatas = {}
        for filename in filenames:
            if not filename.endswith('.txt'):
                raise Exception('Unknown file ending in file "' + filename + '".')
            yearString = filename[:-4]
            if not yearString.isdigit():
                raise Exception('File name "' + filename + '" is not a year.')
            year = int(yearString)
            with open(os.path.join(self.__directory, filename), 'r') as f:
                jsonString = f.read()
            yearData = YearData(year)
            yearData.fromJson(jsonString)
            self.__yearDatas[year] = yearData

    def save(self, year):
        if year not in self.__yearDatas.keys():
            raise Exception('Year ' + str(year) + ' does not exist.')
        jsonString = self.__yearDatas[year].toJson()
        filename = str(year) + '.txt'
        with open(os.path.join(self.__directory, filename), 'w') as f:
            f.write(jsonString)
            
        

    def addYear(self, year):
        if year in self.getYears():
            raise Exception('Year ' + str(year) + ' already exists.')
        self.__yearDatas[year] = YearData(year)

    def getYears(self):
        return list(self.__yearDatas.keys())


    def getYearData(self, year):
        if year not in self.__yearDatas.keys():
            raise Exception('Year ' + str(year) + ' does not exist.')
        return self.__yearDatas[year]
