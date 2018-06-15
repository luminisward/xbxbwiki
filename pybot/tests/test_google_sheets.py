import unittest
from google_sheets import GoogleSheets

class GoogleSheetsCase(unittest.TestCase):

    def setUp(self):
        self.sheet = GoogleSheets()

    def tearDown(self):
        pass

    def test_sheetId(self):
        """Test property sheetId"""
        self.sheet.sheet_id = 'aaa'
        self.assertEqual('aaa', self.sheet.sheet_id)

    def test_range(self):
        """Test property sheetId"""
        self.sheet.range = 'Sheet1'
        self.assertEqual('Sheet1', self.sheet.range)

if __name__ == '__main__':
    unittest.main()
