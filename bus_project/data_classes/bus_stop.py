from typing import List, Any


class BusStop:
    """
    Represents a bus stop with its identifier, latitude, longitude, district and associated lines.

    Attributes:
        stop_id: The identifier of the bus stop.
        stop_lat: The latitude of the bus stop.
        stop_lon: The longitude of the bus stop.
        district: The district of the bus stop.
        lines_list: A list of lines associated with the bus stop.
    """

    __slots__ = ('stop_id', 'stop_lat', 'stop_lon', 'district', 'lines_list')

    def __init__(self, stop_id, stop_lat, stop_lon, district, lines_list):
        self.stop_id = stop_id
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.district = district
        self.lines_list = lines_list

    def get_stop_id(self) -> int:
        """Returns the identifier of the bus stop."""
        return self.stop_id

    def get_stop_lat(self) -> float:
        """Returns the latitude of the bus stop."""
        return self.stop_lat

    def get_stop_lon(self) -> float:
        """Returns the longitude of the bus stop."""
        return self.stop_lon

    def get_stop_district(self) -> str:
        """Returns the district of the bus stop."""
        return self.district

    def get_lines_list(self) -> List[Any]:
        """Returns the list of lines associated with the bus stop."""
        return self.lines_list
