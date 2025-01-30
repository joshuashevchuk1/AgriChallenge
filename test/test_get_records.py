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
        self.assertTrue(top_record.get('precipitation') == 94.0)
        self.assertTrue(top_record.get('station_name') == "USC00110072")

    def test_it_should_get_all_records_for_USC00125237(self):
        records = util.get_records("../src/app/data/wx_data/USC00125237.txt")
        top_record = records[0]
        self.assertTrue(len(records) > 0)
        self.assertTrue(top_record.get('station_name') == "USC00125237")

    def test_it_should_get_all_records_for_USC00126001(self):
        records = util.get_records("../src/app/data/wx_data/USC00126001.txt")
        top_record = records[0]
        self.assertTrue(len(records) > 0)
        self.assertTrue(top_record.get('station_name') == "USC00126001")

    def test_it_should_return_empty_list_for_non_existent_file(self):
        records = util.get_records("../src/app/data/wx_data/non_existent_file.txt")
        self.assertEqual(records, [])

    def test_it_should_return_empty_list_for_empty_file(self):
        records = util.get_records("./empty.txt.py")
        self.assertEqual(records, [])


