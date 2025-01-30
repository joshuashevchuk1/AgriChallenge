import unittest

from app import util

class TestGetRecords(unittest.TestCase):
    def test_it_should_get_all_records_for_USC00110072(self):
        records = util.get_records("../src/app/data/wx_data/USC00110072.txt")
        top_record = records[0]
        self.assertTrue(len(records) > 0)
        self.assertTrue(top_record=={'timestamp': '19850101', 'min_temp': -22.0, 'max_temp': -128.0, 'precipitation': 94.0, 'station_name': 'USC00110072'})
        self.assertTrue(top_record.get('timestamp')=='19850101')
        self.assertTrue(top_record.get('min_temp') == -22.0)
        self.assertTrue(top_record.get('max_temp') == -128.0)
        self.assertTrue(top_record.get('precipitation') == -94.0)
        self.assertTrue(top_record.get('station_name') == "USC00110072")
