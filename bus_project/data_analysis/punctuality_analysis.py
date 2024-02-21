from geopy import distance
from datetime import timedelta, datetime, time
from collections import defaultdict
from typing import List, Tuple, Dict, Union, Any

from bus_project.data_classes.point import Point
from bus_project.data_classes.bus_position import BusPosition
from bus_project.config.config import get_radius, get_time_lower_bound, get_time_upper_bound

RADIUS = get_radius()
TIME_LOWER_BOUND = get_time_lower_bound()
TIME_UPPER_BOUND = get_time_upper_bound()


def get_distance_in_meters(point1: Point, point2: Point) -> float:
    """
    Calculate the distance between two points in meters.
    :param point1: The first point.
    :param point2: The second point.
    :return: The distance between the two points in meters.
    """
    position1 = (point1.latitude, point1.longitude)
    position2 = (point2.latitude, point2.longitude)
    return distance.distance(position1, position2).meters


def get_arrival_time(bus_position_list: List[BusPosition], brigade: str, line: str,
                     stop_point: Point, time_stamp: datetime) -> Union[None, time]:
    """
    Get the bus arrival time at a given stop point.
    :param bus_position_list: List of BusPosition objects.
    :param brigade: Brigade identifier.
    :param line: Bus line identifier.
    :param stop_point: Stop point where the bus is expected to arrive.
    :param time_stamp: Expected arrival time.
    :return: The arrival time of the bus, or None if no bus arrives within the radius.
    """
    minimum_distance = None
    arrival_time = None

    # We are looking for arrivals not earlier than TIME_LOWER_BOUND minutes before planned arrival.
    time_lower_bound = (time_stamp - timedelta(minutes=TIME_LOWER_BOUND)).time()
    time_upper_bound = (time_stamp + timedelta(minutes=TIME_UPPER_BOUND)).time()

    # We iterate through the bus_position_list and find positions which distance from stop is less than RADIUS.
    for bus_position in bus_position_list:
        bus_position_df = bus_position.get_data_frame()

        bus_position_time = bus_position.get_date().time()
        if bus_position_time < time_lower_bound or bus_position_time > time_upper_bound:
            continue

        selected_rows = (bus_position_df['Brigade'] == brigade) & (bus_position_df['Lines'] == line)
        bus_rows = bus_position_df.loc[selected_rows]

        for index, row in bus_rows.iterrows():
            bus_lat = row['Lat']
            bus_lon = row['Lon']
            bus_point = Point(bus_lat, bus_lon)

            dist = get_distance_in_meters(stop_point, bus_point)

            if dist <= RADIUS:
                try:
                    timestamp = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S").time()
                except ValueError:
                    continue

                if timestamp >= time_lower_bound:
                    if minimum_distance is None or dist < minimum_distance:
                        minimum_distance = dist
                        arrival_time = timestamp

    return arrival_time


def handle_correct_arrival(bus_stop_id: str, stop_district: str, stop_point: Point, time_stamp: datetime,
                           time_arrival: time, late_times: List[float],
                           stop_positions: List[Tuple[Point, str]], stop_late_dict: Dict[str, int],
                           district_late_times: Dict[str, List[float]], district_late_dict: Dict[str, int]) -> None:
    """
    Handle the correct arrival of a bus at a stop point.
    :param bus_stop_id: Identifier of the bus stop.
    :param stop_district: District of the bus stop.
    :param stop_point: Stop point where the bus has arrived.
    :param time_stamp: Expected arrival time.
    :param time_arrival: Actual arrival time of the bus.
    :param late_times: List to store late times of bus arrivals.
    :param stop_positions: List to store stop positions where buses are late.
    :param stop_late_dict: Dictionary to store the count of late arrivals for each stop.
    :param district_late_times: Dictionary to store late times for each district.
    :param district_late_dict: Dictionary to store the count of late arrivals for each district.
    :return: None
    """

    arrival_time = datetime.combine(datetime.min, time_arrival)
    expected_time = datetime.combine(datetime.min, time_stamp.time())

    late_time = arrival_time - expected_time
    late_time_minutes = max(0.0, late_time.total_seconds()) / 60

    district_late_times[stop_district].append(late_time_minutes)
    late_times.append(late_time_minutes)

    if late_time_minutes > 0:
        stop_positions.append((stop_point, bus_stop_id))
        stop_late_dict[bus_stop_id] += 1
        if stop_district != '':
            district_late_dict[stop_district] += 1


def get_punctuality(prepared_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyse the punctuality of bus arrivals at each stop point.
    :param prepared_data: A dictionary containing prepared data including bus positions and stop information.
    :return: A dictionary containing punctuality metrics:
            - 'late_times': List of late times for bus arrivals.
            - 'stop_positions': List of stop positions where buses are late.
            - 'stop_late_dict': Dictionary of stop IDs with counts of late arrivals.
            - 'district_late_times': Dictionary with lists of late times for each district.
            - 'district_late_dict': Dictionary with counts of late arrivals for each district.
    """
    bus_position_list = prepared_data['bus_position_list']
    bus_stop_list = prepared_data['bus_stop_list']

    late_times = []
    stop_positions = []
    district_late_times = defaultdict(list)
    district_late_dict = defaultdict(int)
    stop_late_dict = defaultdict(int)

    for bus_stop in bus_stop_list:
        stop_lon = bus_stop.get_stop_lon()
        stop_lat = bus_stop.get_stop_lat()
        stop_point = Point(stop_lat, stop_lon)

        for line_list in bus_stop.get_lines_list():
            line, brigade, time_stamp = line_list

            arrival_time = get_arrival_time(bus_position_list, brigade, line, stop_point, time_stamp)
            maximum_time = (time_stamp + timedelta(minutes=TIME_UPPER_BOUND)).time()

            if arrival_time is not None and arrival_time <= maximum_time:
                handle_correct_arrival(bus_stop.get_stop_id(), bus_stop.get_stop_district(), stop_point, time_stamp,
                                       arrival_time, late_times, stop_positions, stop_late_dict,
                                       district_late_times, district_late_dict)

    punctuality_data = {
        'late_times': late_times,
        'stop_positions': stop_positions,
        'stop_late_dict': stop_late_dict,
        'district_late_times': district_late_times,
        'district_late_dict': district_late_dict,
    }

    return punctuality_data
