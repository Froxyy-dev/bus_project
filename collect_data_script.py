import argparse

from bus_project.data_collecting.gather_bus_data import gather_bus_positions_data
from bus_project.data_collecting.gather_static_data import gather_bus_stop_data


def collect_data(iterations: int, collect_static: bool) -> None:
    if collect_static:
        print("Collecting static data...")
        gather_bus_stop_data()
        print("Finished collecting static data!")

    if iterations > 0:
        print("Collecting bus position data...")
        gather_bus_positions_data(iterations)
        print("Finished collecting bus position data!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("iterations", help="Number of iterations of collecting bus positions.")
    parser.add_argument("collect_static", help="Y to collect static data, N otherwise.")

    args = parser.parse_args()

    collect_data(int(args.iterations), args.collect_static == 'Y')
