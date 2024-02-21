import time
import pandas as pd

from bus_project.data_collecting.helper_functions import get_response, save_df_to_file, wait_if_necessary
from bus_project.data_collecting.url_builders import build_url


def gather_bus_positions_data(iterations: int) -> None:
    """
    Gather bus position data for a specified number of iterations.
    :param iterations: Number of iterations to collect bus position data.
    :return: None
    """
    current_iteration = 0

    while current_iteration < iterations:
        start_time = time.time()

        url = build_url([], 'bus_position_link') + "&type=1"
        bus_info_list = get_response(url)['result']

        current_iteration += 1

        df = pd.DataFrame(bus_info_list, columns=['VehicleNumber', 'Lines', 'Brigade', 'Time', 'Lon', 'Lat'])

        save_df_to_file(df)
        wait_if_necessary(start_time)
