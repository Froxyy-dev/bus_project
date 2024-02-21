# Bus Project

The Bus Project is a package designed for collecting, processing, and analyzing data related to bus traffic in Warsaw. The project consists of several modules that perform various tasks, such as data collection, punctuality analysis, and bus speeding analysis.


## Installation

In order to install library, you need to clone the repository and run:
```bash
    git clone https://github.com/Froxyy-dev/bus_project.git
    cd bus_project
    pip install .
```
## Project structure
Project contains of following parts:

### Config
- bus_project/config

This module contains configuration files used in the project, such as file paths and API keys.

    config.py: Provides configuration parameters and paths used throughout the project.

### Functionalities

- bus_project/data_collecting

This package is designed to gather various types of bus-related data, including both static information about bus stops and real-time bus position data. It consists of several modules that handle different aspects of the data collection process:


    collect_data.py: Collects bus data including static data and bus position data.
    gather_bus_positions_data.py: Gathers bus position data for a specified number of iterations.
    gather_bus_stop_data.py: Gathers data for each bus stop, including lines and detailed information.
    helper_functions.py: This module contains helper functions for handling data retrieval and file management.
    url_builders.py: This module provides a function to build URLs for API requests.

- bus_project/data_preparing

This package provides functions to prepare bus-related data for analysis within a specified time range.:

    prepare_data.py: Provides functions to read bus position and stop information from files and JSON data, 
    as well as for preparing data for analysis within a specified time range.

- bus_project/data_analysis

This package is designed to analyze various aspects of bus-related data collected by the system. It consists of several modules that handle different analysis tasks:

    analyse_all.py: Performs similar analysis to one included in notebook, but saves figures into plots' directory.
    helpers.py: Contains helper functions for various calculations and mappings. 
    punctuality_analysis.py: Performs analysis on the punctuality of bus arrivals at each stop point.
    speeding_analysis.py: Conducts analysis on speeding buses based on prepared data.

- bus_project/data_classes

This package contains classes that represent different aspects of bus-related data:

    bus_position.py: Defines the BusPosition class, representing an entry of bus positions at a specific date and time, 
    along with associated data stored in a DataFrame.
    bus_stop.py: Represents a bus stop with its identifier, latitude, longitude, district and associated lines.
    point.py: Represents a geographical point with latitude and longitude coordinates.

### Analysis
The bus_analysis.ipynb notebook demonstrates an analysis of bus data focusing on both speeding and punctuality aspects. 

Its main components are:

- Data Collection
- Identification of Speeding Incidents
- Quantification of Speeding
- Extremely Fast Buses
- Distribution of Speeding in Districts
- Distribution of Speeding Incidents
- Geospatial Visualization
- Cluster Analysis
- Distribution of Delays
- Distribution of Delays in Districts
- Visualization of Punctual Stops
- Frequency of Delays at Each Stop
- Identification of the Most Delayed Stop
- Number of Stops in each District

### Example usage

    example_usage.py: This script provides a comprehensive example of how to utilize the functionalities of the bus project,
    from data collection to analysis, 
    allowing users to gain insights into bus operations and performance.

### Collect data script

    collect_data_script.py: The collect_data_script.py is a command-line script 
    designed to collect bus data, both static and real-time positions.

To use the collect_data_script.py, you can run it from the command line.

This command will display usage information and available options for the script.

```bash
    python collect_data_script.py --help
```

Here's an example of collecting bus position data for 5 iterations without collecting static data:

```bash
    python collect_data_script.py 5 N
```

### Tests

Unit tests are located in the tests' directory. 
These tests cover various functionalities of the project, including data collection, analysis, and class methods.

- test_data_analysis.py:
This module contains tests of the following functions:

    calculate_distance
    date_difference_in_seconds
    calculate_velocity
    generate_mapping

- test_data_collecting.py:
This module contains tests of the following functions:

    get_response
    get_and_save_response
    wait_if_necessary
    create_directory
    collect_data
    build_url

- test_data_preparing.py:
This module contains tests of the following functions:

    read_bus_position_files
    convert_filename_to_date
    read_bus_stop_info

## Warsaw districts
Warsaw districts geojson file used in project was taken from [here](
https://github.com/andilabs/warszawa-dzielnice-geojson/blob/master/warszawa-dzielnice.geojson).

## Profiler analysis
Profiler stats are stored at profiler_analysis directory. They analyse collecting data as well as preparing and analysing. We can observe that the most time is spent on finding arrival time for each planned stop, however determining point's district is also a demanding operation.

## License

[MIT](LICENSE)