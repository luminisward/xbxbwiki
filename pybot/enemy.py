import json
import csv

class EnemyCSV(object):

    def __init__(self, file):
        self.data = []
        self.file = file
        try:
            with open(file,'r') as f:
                f_csv = csv.DictReader(f)
                for row in f_csv:
                    self.data.append(row)
        except FileNotFoundError:
            open(file,'w').close()

    def readCsvFile(self, file):
        '''Read CSV file, return list[dict]'''
        self.data = []
        with open(file,'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.data.append(row)

    def readJsonFile(self, file):
        '''Read Json file, return list[dict]'''
        self.data = []
        with open(file, 'r') as f:
            self.data = json.load(f)

    def getData(self):
        return self.data

    def saveData(self, headers, dataDict):
        '''Save'''
        with open(self.file,'w') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(dataDict)