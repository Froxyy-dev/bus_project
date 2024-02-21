from bus_project.data_collecting.gather_bus_data import gather_bus_positions_data
from bus_project.data_collecting.gather_static_data import gather_bus_stop_data


def collect_data(iterations: int, collect_static: bool) -> None:
    """
    Collects bus data including static data and bus position data.
    :param iterations: The number of iterations to collect bus position data.
    :param collect_static: Indicates whether to collect static data.
    :return: None
    """
    if collect_static:
        print("Collecting static data...")
        gather_bus_stop_data()
        print("Finished collecting static data!")

    if iterations > 0:
        print("Collecting bus position data...")
        gather_bus_positions_data(iterations)
        print("Finished collecting bus position data!")
