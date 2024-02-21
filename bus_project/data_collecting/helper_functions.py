import requests
import json
import time

from pandas import DataFrame
from typing import Any, Dict, List
from pathlib import Path

from bus_project.data_collecting.url_builders import build_url
from bus_project.config.config import get_bus_positions_path, get_bus_stop_info_path, get_time_to_wait, get_data_path


BUS_POSITIONS_PATH = get_bus_positions_path()
BUS_STOP_INFO_PATH = get_bus_stop_info_path()
TIME_TO_WAIT = get_time_to_wait()
DATA_PATH = get_data_path()


def save_json_to_file(data: Dict[str, Any], filepath: str) -> None:
    """
    Save JSON data to a file.
    :param data: JSON data to be saved.
    :param filepath: Path to file for data to be saved.
    :return: None
    """
    path = Path(DATA_PATH) / filepath
    with open(path, 'w') as file_to_write:
        json.dump(data, file_to_write, indent=4)


def get_response(url: str) -> Dict[str, Any]:
    """
    Get JSON response from a URL.
    :param url: Type of data to get.
    :return: Request response.
    """
    while True:
        try:
            response = requests.get(url).json()
            if not (response is None or type(response['result']) is not list):
                return response
        except Exception:
            continue


def get_and_save_response(arguments: List[str], link: str, filepath: str) -> List[Dict[str, Any]]:
    """
    Get JSON response from a URL and save it to file.
    :param arguments: List of strings to construct url from.
    :param link: Type of data to get.
    :param filepath: Path to file for data to be saved.
    :return: The 'result' field from the response.
    """
    url = build_url(arguments, link)
    response_json = get_response(url)
    save_json_to_file(response_json, filepath)

    return response_json['result']


def get_values_list(values_list: Dict[str, Any]) -> List[Any]:
    """
    Extract a list of values from list of dictionaries.
    :param values_list: List of dictionaries.
    :return: List of values.
    """
    return [item['value'] for item in values_list['values']]


def save_df_to_file(df: DataFrame) -> None:
    """
    Save DataFrame to a CSV file with a timestamped filename.
    :param df: DataFrame to be saved.
    :return: None
    """
    current_time = time.strftime("%D_%H:%M:%S.csv", time.localtime()).replace('/', '-')
    path = DATA_PATH / Path(str(BUS_POSITIONS_PATH) + current_time)
    df.to_csv(path, index=False)


def wait_if_necessary(start_time: float) -> None:
    """
    Wait for the specified time if necessary to adhere to a time interval.
    :param start_time: The start time of the current cycle.
    :return: None
    """
    time_to_wait = float(TIME_TO_WAIT)
    waiting_time = time_to_wait - ((time.time() - start_time) % time_to_wait)
    if waiting_time > 0:
        time.sleep(waiting_time)


def create_directory(bus_stop_id: str, bus_stop_nr: str) -> str:
    """
    Create a directory for bus stop lines if it doesn't exist.
    :param bus_stop_id: Identifier for the bus stop.
    :param bus_stop_nr: Bus stop number.
    :return: The filepath of the created directory.
    """
    filepath = f"{str(BUS_STOP_INFO_PATH)}{bus_stop_id}_{bus_stop_nr}_lines"
    bus_stop_lines_path = DATA_PATH / Path(filepath)

    if not bus_stop_lines_path.exists():
        bus_stop_lines_path.mkdir()

    return filepath
