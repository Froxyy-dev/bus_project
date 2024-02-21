import numpy as np

from collections import defaultdict
from typing import Dict, List, Tuple, Any

from bus_project.data_analysis.helpers import generate_mapping, calculate_distance, \
    calculate_velocity, date_difference_in_seconds
from bus_project.data_classes.point import Point, convert_position
from bus_project.data_classes.bus_position import BusPosition
from bus_project.config.config import get_speed_limit, get_maximum_speed
from bus_project.data_preparing.prepare_data import get_warsaw_district

SPEED_LIMIT = get_speed_limit()
MAXIMUM_SPEED = get_maximum_speed()


def extract_position_data(bus_position_list: List[BusPosition], bus_id_list_len: int,
                          nr_to_idx: Dict[int, int]) -> Tuple[List[Any], List[List[Any]]]:
    """
    Extract position data from bus position list.
    :param bus_position_list: List of BusPosition objects.
    :param bus_id_list_len: Length of the bus ID list.
    :param nr_to_idx: Dictionary mapping bus numbers to indices.
    :return: A tuple containing:
            - bus_positions_array: List of numpy arrays representing bus positions.
            - bus_update_time: List of lists containing bus update times.
    """
    bus_positions_array = []
    bus_update_time = []

    for bus_position in bus_position_list:
        bus_position_df = bus_position.get_data_frame()
        bus_position_np = bus_position_df[['VehicleNumber', 'Lat', 'Lon', 'Time']].to_numpy()

        bus_array = np.zeros((bus_id_list_len, 2))
        bus_update_list = [None] * bus_id_list_len

        for current_position in bus_position_np:
            try:
                vehicle_number = nr_to_idx[int(current_position[0])]
            except ValueError:
                vehicle_number = 0

            bus_array[vehicle_number] = (max(min(90, current_position[1]), -90), max(min(90, current_position[2]), -90))
            bus_update_list[vehicle_number] = current_position[-1]

        bus_positions_array.append(bus_array)
        bus_update_time.append(bus_update_list)

    return bus_positions_array, bus_update_time


def validate(time_str: str) -> bool:
    """
    Validate the time string format.
    :param time_str: Time string.
    :return: True if the time string is valid, False otherwise.
    """
    return time_str is not None and len(time_str) == 19


def calculate_difference_arrays(bus_positions_array: List[np.ndarray], bus_update_time: List[List[str]],
                                bus_id_list_len: int) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Calculate difference arrays for bus positions and update times.
    :param bus_positions_array: List of numpy arrays representing bus positions.
    :param bus_update_time: List of lists containing bus update times.
    :param bus_id_list_len: Length of the bus ID list.
    :return: A tuple containing:
            - bus_distances_array: List of numpy arrays representing distance differences.
            - time_difference_array: List of numpy arrays representing time differences.
    """
    bus_distances_array = []
    time_difference_array = []

    for i in range(1, len(bus_positions_array)):
        distance_array = calculate_distance(bus_positions_array[i], bus_positions_array[i - 1])

        bus_distances_array.append(distance_array)

    for i in range(1, len(bus_update_time)):
        update_time_array = np.zeros(bus_id_list_len)

        for j in range(bus_id_list_len):
            if validate(bus_update_time[i][j]) and validate(bus_update_time[i-1][j]):
                update_time_array[j] = date_difference_in_seconds(bus_update_time[i - 1][j], bus_update_time[i][j])
            else:
                update_time_array[j] = 0

        time_difference_array.append(update_time_array)

    return bus_distances_array, time_difference_array


def get_speeding(bus_distances_array: List[np.array], time_difference_array: List[np.array], bus_id_list_len: int,
                 idx_to_nr: Dict[int, int], bus_position_array: List[np.ndarray]) \
        -> Tuple[int, List[Point], List[int], int, int, List[float], Dict[str, int]]:
    """
    Analyse speeding buses.
    :param bus_distances_array: List of numpy arrays representing distance differences.
    :param time_difference_array: List of numpy arrays representing time differences.
    :param bus_id_list_len: Length of the bus ID list.
    :param idx_to_nr: Dictionary mapping indices to bus numbers.
    :param bus_position_array: List of numpy arrays representing bus positions.
    :return: A tuple containing:
            - speeding_count: The count of speeding buses.
            - points: List of points representing the speeding buses' positions.
            - speeding_buses: List of speeding bus numbers.
            - number_measured: The number of movements measured for speeding.
            - number_rejected: The number of movements rejected.
            - speed_array: List of speeds for each measured movement.
            - district_speeding_points: Dictionary containing counts of speeding buses in each district.
    """
    speeding_count = 0
    number_measured = 0
    number_rejected = 0
    points = []
    speeding_buses = []
    speed_array = []

    district_speeding_points = defaultdict(int)

    for bus in range(bus_id_list_len):
        # We count the number of maximum subarray which values are greater than 50.
        current_length = 0
        first_point = Point(-1, -1)

        for transition in range(len(bus_distances_array)):
            distance = bus_distances_array[transition][bus]
            time_difference = time_difference_array[transition][bus]

            if time_difference == 0:    # Data has not yet been updated.
                continue

            velocity = calculate_velocity(distance, time_difference)

            if velocity > MAXIMUM_SPEED:
                number_rejected += 1
                continue

            number_measured += 1
            speed_array.append(velocity)

            last_point = convert_position(bus_position_array[transition][bus])

            if velocity <= SPEED_LIMIT:
                if current_length > 0:
                    speeding_count += 1
                    speeding_buses.append(idx_to_nr[bus])

                    mean_point = first_point.average(last_point)
                    mean_point_district = get_warsaw_district(mean_point)
                    points.append(mean_point)

                    if mean_point_district != '':
                        district_speeding_points[mean_point_district] += 1

                current_length = 0
            else:
                if first_point == Point(-1, -1):
                    first_point = convert_position(bus_position_array[transition][bus])

                current_length += 1

        if current_length > 0:
            speeding_count += 1
            speeding_buses.append(idx_to_nr[bus])

            last_point = convert_position(bus_position_array[len(bus_distances_array)][bus])
            mean_point = first_point.average(last_point)
            mean_point_district = get_warsaw_district(mean_point)
            points.append(mean_point)

            if mean_point_district != '':
                district_speeding_points[mean_point_district] += 1

    return (speeding_count, points, speeding_buses, number_measured,
            number_rejected, speed_array, district_speeding_points)


def get_speeding_analysis(prepared_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform speeding analysis based on prepared data.
    :param prepared_data: A dictionary containing prepared data including bus positions and stop information.
    :return: A dictionary containing speeding analysis results:
            - 'speeding_count': The count of speeding buses.
            - 'number_measured': The number of buses measured for speeding.
            - 'number_rejected': The number of movements rejected.
            - 'speeding_points': List of points representing the speeding buses' positions.
            - 'speeding_buses': List of speeding bus numbers.
            - 'nr_to_idx': Dictionary mapping bus numbers to indices.
            - 'idx_to_nr': Dictionary mapping indices to bus numbers.
            - 'distinct_buses': Set of distinct speeding bus numbers.
    """
    bus_id_list = prepared_data['bus_id_list']
    bus_position_list = prepared_data['bus_position_list']
    bus_id_list_len = len(bus_id_list)

    nr_to_idx, idx_to_nr = generate_mapping(bus_id_list)

    bus_positions_array, bus_update_time = extract_position_data(bus_position_list, bus_id_list_len, nr_to_idx)

    bus_distances_array, time_difference_array = calculate_difference_arrays(bus_positions_array, bus_update_time,
                                                                             bus_id_list_len)

    (speeding_count, speeding_points, speeding_buses, number_measured, number_rejected, speed_array,
     district_speeding_points) = get_speeding(bus_distances_array, time_difference_array,
                                              bus_id_list_len, idx_to_nr, bus_positions_array)

    distinct_buses = set(speeding_buses)

    speeding_data = {
        'speeding_count': speeding_count,
        'number_measured': number_measured,
        'number_rejected': number_rejected,
        'speeding_points': speeding_points,
        'speeding_buses': speeding_buses,
        'nr_to_idx': nr_to_idx,
        'idx_to_nr': idx_to_nr,
        'distinct_buses': distinct_buses,
        'speed_array': speed_array,
        'district_speeding_points': district_speeding_points,
    }

    return speeding_data
