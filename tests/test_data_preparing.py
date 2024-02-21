import unittest
from datetime import datetime
from pathlib import Path
import pandas as pd
from unittest.mock import patch
from bus_project.data_preparing.prepare_data import (read_bus_position_files, convert_filename_to_date,
                                                     read_bus_stop_info, get_warsaw_district)
from bus_project.data_classes.bus_position import BusPosition
from bus_project.data_classes.bus_stop import BusStop
from bus_project.data_classes.point import Point
from bus_project.config import config


class TestDataPreparing(unittest.TestCase):

    @patch('bus_project.data_preparing.prepare_data.convert_filename_to_date')
    @patch('bus_project.data_preparing.prepare_data.pd.read_csv')
    def test_read_bus_position_files(self, mock_read_csv, mock_convert_filename_to_date):
        test_data_path = Path("test_data")
        test_data_path.mkdir(exist_ok=True)
        test_csv_file1 = test_data_path / "test_file1.csv"
        test_csv_file2 = test_data_path / "test_file2.csv"

        data1 = {
            'VehicleNumber': [1, 2, 3],
            'Timestamp': [datetime(2024, 2, 16, 8, 0, 0), datetime(2024, 2, 16, 9, 0, 0),
                          datetime(2024, 2, 16, 10, 0, 0)]
        }
        data2 = {
            'VehicleNumber': [4, 5, 6],
            'Timestamp': [datetime(2024, 2, 17, 8, 0, 0), datetime(2024, 2, 17, 9, 0, 0),
                          datetime(2024, 2, 17, 10, 0, 0)]
        }

        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        df1.to_csv(test_csv_file1, index=False)
        df2.to_csv(test_csv_file2, index=False)

        mock_read_csv.side_effect = [df1, df2]

        mock_convert_filename_to_date.side_effect = [datetime(2024, 2, 16), datetime(2024, 2, 17)]

        start_time = datetime(2024, 2, 16)
        end_time = datetime(2024, 2, 17)
        bus_position_list, bus_id_set = read_bus_position_files(test_data_path, start_time, end_time)

        expected_bus_position_list = [
            BusPosition(datetime(2024, 2, 16), df1),
            BusPosition(datetime(2024, 2, 17), df2)
        ]
        expected_bus_id_set = {1, 2, 3, 4, 5, 6}

        self.assertEqual(len(bus_position_list), len(expected_bus_position_list))
        self.assertEqual(sorted(bus_position_list), sorted(expected_bus_position_list))
        self.assertEqual(bus_id_set, expected_bus_id_set)

        test_csv_file1.unlink()
        test_csv_file2.unlink()
        test_data_path.rmdir()

    def test_convert_filename_to_date(self):
        filename = "01-01-22_12:30:00"
        expected_date = datetime(2022, 1, 1, 12, 30, 0)
        result_date = convert_filename_to_date(filename)
        self.assertEqual(result_date, expected_date)

        filename = "12-31-21_23:59:59"
        expected_date = datetime(2021, 12, 31, 23, 59, 59)
        result_date = convert_filename_to_date(filename)
        self.assertEqual(result_date, expected_date)

        filename = "06-15-23_08:45:30"
        expected_date = datetime(2023, 6, 15, 8, 45, 30)
        result_date = convert_filename_to_date(filename)
        self.assertEqual(result_date, expected_date)

    def test_read_bus_stop_info(self):
        bus_stop_list_path = config.get_data_path() / config.get_bus_stop_list_json()
        start_time = datetime.strptime("08:00:00", "%H:%M:%S")
        end_time = datetime.strptime("8:01:00", "%H:%M:%S")

        bus_stops = read_bus_stop_info(bus_stop_list_path, start_time, end_time, False)

        self.assertIsInstance(bus_stops, list)
        for bus_stop in bus_stops:
            self.assertIsInstance(bus_stop, BusStop)
            self.assertIsInstance(bus_stop.get_stop_id(), str)
            self.assertIsInstance(bus_stop.get_lines_list(), list)
            for line_info in bus_stop.get_lines_list():
                self.assertIsInstance(line_info, list)
                self.assertEqual(len(line_info), 3)
                self.assertIsInstance(line_info[0], str)  # Line name
                self.assertIsInstance(line_info[1], str)  # Brigade
                self.assertIsInstance(line_info[2], datetime)  # Time stamp
                self.assertTrue(start_time.time() <= line_info[2].time() <= end_time.time())

    def test_point_inside_district(self):
        point_inside = Point(52.2324, 21.0162)

        result = get_warsaw_district(point_inside)
        self.assertEqual(result, "Śródmieście")

    def test_point_outside_district(self):
        point_outside = Point(42, 42)

        result = get_warsaw_district(point_outside)
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
