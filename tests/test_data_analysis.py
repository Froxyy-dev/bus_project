import pytest
import numpy as np

from bus_project.data_analysis.helpers import calculate_distance, date_difference_in_seconds, \
                                              calculate_velocity, generate_mapping
from bus_project.data_analysis.punctuality_analysis import get_distance_in_meters
from bus_project.data_classes.point import Point


class TestDataAnalysis:
    @pytest.mark.parametrize("np_arr1, np_arr2, expected", [
        (np.array([[0, 0]]), np.array([[1, 1]]), 157.249)
    ])
    def test_calculate_distance(self, np_arr1, np_arr2, expected):
        assert abs(calculate_distance(np_arr1, np_arr2)[0] - expected) < 3

    @pytest.mark.parametrize("date_str1, date_str2, expected", [
        ("2024-02-16 10:00:00", "2024-02-16 11:00:00", 3600)
    ])
    def test_date_difference_in_seconds(self, date_str1, date_str2, expected):
        assert date_difference_in_seconds(date_str1, date_str2) == expected

    @pytest.mark.parametrize("distance_covered, time, expected", [
        (100, 10, 36000.0)
    ])
    def test_calculate_velocity(self, distance_covered, time, expected):
        assert calculate_velocity(distance_covered, time) == expected

    @pytest.mark.parametrize("bus_id_list, expected_nr_to_idx, expected_idx_to_nr", [
        ([1, 2, 3], {1: 0, 2: 1, 3: 2}, {0: 1, 1: 2, 2: 3})
    ])
    def test_generate_mapping(self, bus_id_list, expected_nr_to_idx, expected_idx_to_nr):
        nr_to_idx, idx_to_nr = generate_mapping(bus_id_list)
        assert nr_to_idx == expected_nr_to_idx
        assert idx_to_nr == expected_idx_to_nr

    def test_same_point(self):
        point1 = Point(52.2324, 21.0162)
        point2 = Point(52.2324, 21.0162)

        result = get_distance_in_meters(point1, point2)
        assert result == 0

    def test_different_points(self):
        point1 = Point(52.211821, 20.981944)    # Very interesting place.
        point2 = Point(52.231918, 21.006781)

        expected_result = 2800
        result = get_distance_in_meters(point1, point2)
        assert abs(result - expected_result) < 100
