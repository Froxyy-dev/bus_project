from itertools import chain
from bus_project.config.config import get_api_key
from typing import List

API_KEY = get_api_key()


URLS = {
    'bus_position_link': [
        'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59&apikey=',
    ],
    'bus_stops_link': [
        'https://api.um.warszawa.pl/api/action/dbstore_get/?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630&apikey='
    ],
    'bus_stop_lines_link': [
        'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId=',
        '&busstopNr=',
        '&apikey=',
    ],
    'line_at_bus_stop_link': [
        'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=',
        '&busstopNr=',
        '&line=',
        '&apikey=',
    ],
}


def build_url(arguments: List[str], link: str) -> str:
    """
    Build URL by combining the base URL and provided arguments.
    :param arguments: List of arguments to be added to the URL.
    :param link: Key for selecting the URL from the predefined ones.
    :return: Constructed URL as a string.
    """
    arguments.append(API_KEY)
    chained_list = list(chain.from_iterable(zip(URLS[link], arguments)))
    return ''.join(chained_list)
