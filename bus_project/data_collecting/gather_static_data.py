from bus_project.data_collecting.helper_functions import get_and_save_response, get_values_list, create_directory
from bus_project.config import config


BUS_STOP_INFO_PATH = config.get_bus_stop_info_path()


def gather_bus_stop_data() -> None:
    """
    Gather data for each bus stop, including lines and detailed information.
    :return: None
    """
    # 1. Fetch the list of bus stops.
    bus_stops = get_and_save_response([], 'bus_stops_link', 'bus_stop_list.json')

    for bus_stop_values in bus_stops:
        # 2. For each bus stop, get the lines passing through and save the data.
        bus_stop_id, bus_stop_nr, bus_stop_name, *_ = get_values_list(bus_stop_values)
        arguments = [bus_stop_id, bus_stop_nr]
        filepath_to_save = f"{str(BUS_STOP_INFO_PATH)}{bus_stop_id}_{bus_stop_nr}.json"

        bus_stop_lines = get_and_save_response(arguments, 'bus_stop_lines_link', filepath_to_save)
        bus_stop_dir_path = create_directory(bus_stop_id, bus_stop_nr)

        for bus_stop_line_values in bus_stop_lines:
            # 3. For each line at a bus stop, gather detailed information and save the data.
            bus_stop_line_nr = get_values_list(bus_stop_line_values)[0]
            arguments = [bus_stop_id, bus_stop_nr, bus_stop_line_nr]

            bus_stop_filepath = bus_stop_dir_path + f"/{bus_stop_line_nr}.json"
            get_and_save_response(arguments, 'line_at_bus_stop_link', bus_stop_filepath)
