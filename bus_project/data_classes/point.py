from geopy import distance
from typing import Tuple


class Point:
    """
    Represents a geographical point with latitude and longitude coordinates.

    Attributes:
        latitude: The latitude coordinate of the point.
        longitude: The longitude coordinate of the point.

    Methods:
        distance(other):
        average(other): Calculates the midpoint between this Point and another Point.
    """
    __slots__ = ('latitude', 'longitude')

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other) -> bool:
        return self.latitude == other.latitude and self.longitude == other.longitude

    def distance(self, other) -> float:
        """Calculates the distance between this Point and another Point in kilometers."""
        position1 = (self.latitude, self.longitude)
        position2 = (other.latitude, other.longitude)
        return distance.distance(position1, position2).km

    def average(self, other):
        """Calculates the midpoint between this Point and another Point."""
        return Point((self.latitude + other.latitude) / 2, (self.longitude + other.longitude) / 2)


def convert_position(position: Tuple[float, float]) -> Point:
    """
    Convert a position to a Point object.
    :param position: A tuple containing latitude and longitude coordinates.
    :return: A Point object representing the position.
    """
    return Point(position[0], position[1])
