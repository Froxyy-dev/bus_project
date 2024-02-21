import numpy as np

from geopy import distance
from itertools import starmap
from datetime import datetime
from typing import List, Tuple

from bus_project.config.config import get_data_path

DATA_PATH = get_data_path()


def calculate_distance(np_arr1: np.ndarray, np_arr2: np.ndarray) -> np.ndarray:
    """
    Calculate the distance between pairs of points represented by
    two NumPy arrays of latitude and longitude coordinates.
    :param np_arr1: NumPy array containing latitude and longitude coordinates of the first set of points.
    :param np_arr2: NumPy array containing latitude and longitude coordinates of the second set of points.
    :return: NumPy array containing the distances between corresponding pairs of points.
    """
    points = list(zip(np_arr1, np_arr2))
    distance_list = [i.km for i in starmap(distance.distance, points)]
    return np.array(distance_list)


def date_difference_in_seconds(date_str1: str, date_str2: str) -> float:
    """
    Calculate the time difference in seconds between two datetime strings.
    :param date_str1: A string representing the first datetime.
    :param date_str2: A string representing the second datetime.
    :return: The time difference in seconds.
    """
    date_format = "%Y-%m-%d %H:%M:%S"
    datetime1 = datetime.strptime(date_str1, date_format)
    datetime2 = datetime.strptime(date_str2, date_format)

    time_difference_seconds = (datetime2 - datetime1).total_seconds()

    return time_difference_seconds


def calculate_velocity(distance_covered: float, time: float) -> float:
    """
    Calculate the velocity given the distance covered and the time taken.
    :param distance_covered: The distance covered in kilometers.
    :param time: The time taken to cover the distance in seconds.
    :return: The velocity in kilometers per hour (km/h).
    """
    return (distance_covered * 3600.0) / time


def generate_mapping(bus_id_list: List[str]) -> Tuple[dict, dict]:
    """
    Generate mappings between bus IDs and their corresponding indices.
    :param bus_id_list: List of bus IDs.
    :return: A tuple containing two dictionaries:
            - nr_to_idx: Mapping from bus ID to index.
            - idx_to_nr: Mapping from index to bus ID.
    """
    nr_to_idx = {}
    idx_to_nr = {}

    for i in range(len(bus_id_list)):
        nr_to_idx[bus_id_list[i]] = i
        idx_to_nr[i] = bus_id_list[i]

    return nr_to_idx, idx_to_nr
