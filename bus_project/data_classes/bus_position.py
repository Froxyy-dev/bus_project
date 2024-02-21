from datetime import datetime
from pandas import DataFrame


class BusPosition:
    """
    Represents an entry of bus positions at a specific date and time, along with associated data in a DataFrame.

    Attributes:
        date: The date and time of gathering data.
        data_frame: The DataFrame containing associated data.
    """

    __slots__ = ('date', 'data_frame')

    def __init__(self, date, data_frame):
        self.date = date
        self.data_frame = data_frame

    def __eq__(self, other) -> bool:
        return self.date == other.date

    def __lt__(self, other) -> bool:
        return self.date < other.date

    def get_date(self) -> datetime:
        """Returns the date and time of the bus position."""
        return self.date

    def get_data_frame(self) -> DataFrame:
        """Returns the DataFrame containing associated data."""
        return self.data_frame
