from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager


# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()
flight_search = FlightSearch(sheet_data)
# flight_search.check_iata_codes()
sheet_data = flight_search.data
# data_manager.update_sheet(sheet_data)
flight_search.get_available_flights()
notification = NotificationManager()
pprint(sheet_data)

flight_data = flight_search.flight_info
print(flight_data)
for data in sheet_data:
    try:
        flight: FlightData = flight_data[data["iataCode"]]
    except KeyError:
        continue
    else:
        if float(flight.price) <= float(data["lowestPrice"]):
            message = notification.create_alert(flight)
            notification.send_message(message)
            notification.send_emails(message, data_manager.get_users_emails())
