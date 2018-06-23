from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleSheets(object):

    def __init__(self):
        self.__SPREADSHEET_ID = ''
        self.__RANGE_NAME = ''
        self.__raw_data = []

        # Setup the Sheets API
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.__service = build('sheets', 'v4', http=creds.authorize(Http()))

    @property
    def sheet_id(self):
        return self.__SPREADSHEET_ID

    @sheet_id.setter
    def sheet_id(self, value):
        self.__SPREADSHEET_ID = value

    @property
    def range(self):
        return self.__RANGE_NAME

    @range.setter
    def range(self, value):
        self.__RANGE_NAME = value

    def pull_data(self):
        # Call the Sheets API
        result = self.__service.spreadsheets().values().get(
            spreadsheetId=self.__SPREADSHEET_ID, range=self.__RANGE_NAME
            ).execute()
        self.__raw_data = result.get('values', [])

    @property
    def dict_list(self):
        table_header = self.__raw_data[0]
        table_body = self.__raw_data[1:]
        ret = []
        for row in table_body:
            row = zip(table_header, row)
            row = dict(row)
            ret.append(row)
        return ret
