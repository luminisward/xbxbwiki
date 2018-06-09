from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleSheets(object):

    def __init__(self):
        self.__SPREADSHEET_ID = ''
        self.__RANGE_NAME = ''
        self.__rawData = []
        
        # Setup the Sheets API
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.__service = build('sheets', 'v4', http=creds.authorize(Http()))

    @property
    def sheetId(self):
        return self.__SPREADSHEET_ID

    @sheetId.setter
    def sheetId(self, value):
        self.__SPREADSHEET_ID = value

    @property
    def range(self):
        return self.__RANGE_NAME

    @sheetId.setter
    def range(self, value):
        self.__RANGE_NAME = value

    def pullData(self):
        # Call the Sheets API
        result = self.__service.spreadsheets().values().get(spreadsheetId=self.__SPREADSHEET_ID,range=self.__RANGE_NAME).execute()
        self.__rawData = result.get('values', [])

    @property
    def dictList(self):
        tableHeader = self.__rawData.pop(0)
        tableBody = []
        for row in self.__rawData:
            row = zip(tableHeader, row)
            row = dict(row)
            tableBody.append(row)
        return tableBody
