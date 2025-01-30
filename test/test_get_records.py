import unittest

from app import util

class TestGetRecords(unittest.TestCase):
    def test_get_records_not_empty(self):
        records = util.get_records("../src/app/data/wx_data/USC00110072.txt")
