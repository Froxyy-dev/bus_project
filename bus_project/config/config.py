from pathlib import Path

# PATHS TO DIRECTORIES #
PROJECT_PATH = Path(__file__).parents[2]

DATA_PATH = PROJECT_PATH / 'data'
PLOTS_PATH = PROJECT_PATH / 'plots'

# RELATIVE PATHS TO DIRECTORIES #
BUS_POSITIONS_PATH = 'bus_positions/'
BUS_STOP_INFO_PATH = 'bus_stop_info/'
WARSAW_DISTRICTS_PATH = 'warsaw_districts/'

# FILENAMES #
BUS_STOP_LIST_JSON = 'bus_stop_list.json'
WARSAW_DISTRICTS_GEOJSON = 'warszawa-dzielnice.geojson'

# API KEY #
API_KEY = '84d234ff-041e-4204-84b5-3d15c5a0aa22'    # <-- Update with your own one.

# CONSTANT VALUES #
WARSAW_LATITUDE = 52.2282143
WARSAW_LONGITUDE = 21.0856586

TIME_TO_WAIT = 20

RADIUS = 50
TIME_LOWER_BOUND = 4
TIME_UPPER_BOUND = 15

SPEED_LIMIT = 50
MAXIMUM_SPEED = 90


def get_data_path() -> Path:
    """
    Get the path to the data directory.
    :return: The path to the data directory.
    """
    return DATA_PATH


def get_plots_path() -> Path:
    """
    Get the path to the plots' directory.
    :return: The path to the plots' directory.
    """
    return PLOTS_PATH


def get_bus_positions_path() -> str:
    """
    Get the relative path to the bus positions directory.
    :return: The relative path to the bus positions directory.
    """
    return BUS_POSITIONS_PATH


def get_bus_stop_info_path() -> str:
    """
    Get the relative path to the bus stop info directory.
    :return: The relative path to the bus stop info directory.
    """
    return BUS_STOP_INFO_PATH


def get_warsaw_districts_path() -> str:
    """
    Get the relative path to the Warsaw districts directory.
    :return: The relative path to the Warsaw districts directory.
    """
    return WARSAW_DISTRICTS_PATH


def get_bus_stop_list_json() -> str:
    """
    Get the filename of the bus stop list JSON file.
    :return: The filename of the bus stop list JSON file.
    """
    return BUS_STOP_LIST_JSON


def get_warsaw_districts_geojson() -> str:
    """
    Get the filename of the Warsaw districts GeoJSON file.
    :return: The filename of the Warsaw districts GeoJSON file.
    """
    return WARSAW_DISTRICTS_GEOJSON


def get_api_key() -> str:
    """
    Get the API key for accessing Warsaw buses requests.
    :return: The API key.
    """
    return API_KEY


def get_warsaw_latitude() -> float:
    """
    Get the latitude of Warsaw.
    :return: The latitude of Warsaw.
    """
    return WARSAW_LATITUDE


def get_warsaw_longitude() -> float:
    """
    Get the longitude of Warsaw.
    :return: The longitude of Warsaw.
    """
    return WARSAW_LONGITUDE


def get_time_to_wait() -> int:
    """
    Get the time to wait between data collection cycles.
    :return: The time to wait in seconds.
    """
    return TIME_TO_WAIT


def get_radius() -> int:
    """
    Get the radius used for matching positions to stops.
    :return: The radius in meters.
    """
    return RADIUS


def get_time_lower_bound() -> int:
    """
    Get the lower bound for the time window used for estimating bus arrival times.
    :return: The lower bound time in minutes.
    """
    return TIME_LOWER_BOUND


def get_time_upper_bound() -> int:
    """
    Get the upper bound for the time window used for estimating bus arrival times.
    :return: The upper bound time in minutes.
    """
    return TIME_UPPER_BOUND


def get_speed_limit() -> int:
    """
    Get the speed limit for buses in kilometers per hour.
    :return: The speed limit in km/h.
    """
    return SPEED_LIMIT


def get_maximum_speed() -> int:
    """
    Get the maximum reasonable speed for buses in kilometers per hour.
    :return: The maximum speed in km/h.
    """
    return MAXIMUM_SPEED
