import pandas as pd

from bus_project.data_preparing.prepare_data import get_prepared_data
from bus_project.data_analysis.speeding_analysis import get_speeding_analysis
from bus_project.data_analysis.punctuality_analysis import get_punctuality


start_time = pd.Timestamp(year=2024, month=2, day=19, hour=22, minute=0)
end_time = pd.Timestamp(year=2024, month=2, day=19, hour=22, minute=20)

prepared_data = get_prepared_data(start_time, end_time, True)
bus_id_list_len = len(prepared_data['bus_id_list'])
print(f"Liczba autobusow: {bus_id_list_len}")

speeding_data = get_speeding_analysis(prepared_data)
distinct_buses = len(speeding_data['distinct_buses'])
print(f"Liczba autobusów, które przekroczyły 50 km/h: {distinct_buses}")

punctuality_data = get_punctuality(prepared_data)
stop_positions = punctuality_data['stop_positions']
print(f"Liczba spóźnień autobusów: {len(stop_positions)}")
