import pandas as pd
import json
import geojson

from shapely import geometry
from typing import List, Tuple, Set, Dict, Union
from pathlib import Path
from datetime import datetime

from bus_project.data_classes.bus_position import BusPosition
from bus_project.data_classes.bus_stop import BusStop
from bus_project.data_classes.point import Point
from bus_project.config.config import (get_bus_positions_path, get_bus_stop_info_path, get_data_path,
                                       get_bus_stop_list_json, get_warsaw_districts_path, get_warsaw_districts_geojson)

BUS_POSITIONS_PATH = get_bus_positions_path()
BUS_STOP_INFO_PATH = get_bus_stop_info_path()
DATA_PATH = get_data_path()
BUS_STOP_LIST_JSON = get_bus_stop_list_json()
WARSAW_DISTRICTS_PATH = get_warsaw_districts_path()
WARSAW_DISTRICTS_GEOJSON = get_warsaw_districts_geojson()


def get_warsaw_district(point: Point) -> str:
    """
    Retrieves the Warsaw district name for a given geographical point.
    :param point: A Point object representing the geographical coordinates (latitude and longitude) of the point.
    :return: The name of the Warsaw district in which the point is located, otherwise an empty string.
    """
    warsaw_districts_filename = DATA_PATH / WARSAW_DISTRICTS_PATH / WARSAW_DISTRICTS_GEOJSON
    with open(warsaw_districts_filename, 'r') as file:
        warsaw_districts_geojson = geojson.load(file)
    warsaw_districts_list = warsaw_districts_geojson['features']

    point_district = ''
    point_location = geometry.Point(point.longitude, point.latitude)

    for warsaw_district in warsaw_districts_list[1:]:
        district_coordinates = warsaw_district['geometry']['coordinates']
        warsaw_district_polygon = geometry.MultiPolygon(district_coordinates)

        if warsaw_district_polygon.contains(point_location):
            point_district = warsaw_district['properties']['name']
            break

    return point_district


def convert_filename_to_date(filename: str) -> datetime:
    """
    Convert filename string to a datetime object.
    :param filename: The filename to be converted, expected in format "MM-DD-YY_HH:MM:SS".
    :return: A datetime object representing the date from the filename.
    """
    date_format = "%m-%d-%y_%H:%M:%S"
    return datetime.strptime(filename, date_format)


def read_bus_position_files(path: Path, start_time: datetime, end_time: datetime) -> Tuple[List[BusPosition], Set[str]]:
    """
    Read bus position files from the specified path and filter data based on start and end times.
    :param path: The path where the bus position files are located.
    :param start_time: The start time to filter the data.
    :param end_time: The end time to filter the data.
    :return: List of BusPosition objects and a set of unique bus IDs.
    """
    files = path.glob('*.csv')

    bus_position_list = []
    bus_id_set = set()

    for file_path in files:
        date = convert_filename_to_date(file_path.stem)
        if date < start_time or date > end_time:
            continue

        df = pd.read_csv(file_path)
        current_set = set(df['VehicleNumber'])

        bus_id_set = bus_id_set.union(current_set)
        bus_position = BusPosition(date, df)

        bus_position_list.append(bus_position)

    return bus_position_list, bus_id_set


def read_bus_stop_info(bus_stop_list_path: Path, start_time: datetime,
                       end_time: datetime, get_districts: bool) -> List[BusStop]:
    """
    Read bus stop information from JSON files and filter data based on start and end times.
    :param bus_stop_list_path: The path to the JSON file containing bus stop information.
    :param start_time: The start time to filter the data.
    :param end_time: The end time to filter the data.
    :param get_districts: Flag indicating if we want to gather districts.
    :return: A list of BusStop objects representing bus stop information.
    """
    bus_stop_list = []

    with open(bus_stop_list_path, 'r') as file:
        for bus_stop_values in json.load(file)['result']:
            values_list = [item['value'] for item in bus_stop_values['values']]
            bus_stop_id, bus_stop_nr, stop_lat, stop_lon = values_list[0:2] + values_list[4:6]

            district = ''

            if get_districts:
                district = get_warsaw_district(Point(stop_lat, stop_lon))

            stop_id = f"{bus_stop_id}_{bus_stop_nr}"
            stop_id_path = DATA_PATH / f"{str(BUS_STOP_INFO_PATH)}{stop_id}_lines/"
            bus_stop_lines_list = []

            for line in stop_id_path.glob('*.json'):
                with open(line, 'r') as line_file:
                    for time_slot in json.load(line_file)['result']:
                        values_list = [item['value'] for item in time_slot['values']]
                        brigade, time_stamp = (values_list[2], values_list[5])
                        if '00:00:00' <= time_stamp < '24:00:00':
                            time_stamp = datetime.strptime(time_stamp, '%H:%M:%S')
                            if start_time.time() <= time_stamp.time() <= end_time.time():
                                bus_stop_lines_list.append([line.stem, brigade, time_stamp])

            bus_stop_list.append(BusStop(stop_id, stop_lat, stop_lon, district, bus_stop_lines_list))

    return bus_stop_list


def get_prepared_data(start_time: datetime, end_time: datetime,
                      get_districts: bool) -> Dict[str, Union[List[BusPosition], Set[str], List[BusStop]]]:
    """
    Get prepared data for the specified time range.
    :param start_time: The start time of the data to collect.
    :param end_time: The end time of the data to collect.
    :param get_districts: Flag indicating if we want to gather districts.
    :return: A dictionary containing the prepared data, including bus position list,
              list of bus IDs, and bus stop list.
    """
    bus_position_path = DATA_PATH / Path(str(BUS_POSITIONS_PATH))
    bus_stop_list_path = DATA_PATH / BUS_STOP_LIST_JSON

    bus_position_list, bus_id_set = read_bus_position_files(bus_position_path, start_time, end_time)

    bus_stop_list = read_bus_stop_info(bus_stop_list_path, start_time, end_time, get_districts)

    prepared_data = {
        'bus_position_list': sorted(bus_position_list),
        'bus_id_list': sorted(bus_id_set),
        'bus_stop_list': bus_stop_list
    }

    return prepared_data
