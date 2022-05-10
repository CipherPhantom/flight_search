import requests
import datetime as dt
from flight_data import FlightData

TEQUILA_LOCATIONS_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
LOCATION_IATA_CODE = "LON"
CURRENCY = "GBP"

# Dates
now = dt.datetime.now()
TOMORROW = (now + dt.timedelta(days=1)).strftime("%d/%m/%Y")
IN_6_MONTHS = (now + dt.timedelta(days=6*30)).strftime("%d/%m/%Y")
IN_7_DAYS = (now + dt.timedelta(days=7)).strftime("%d/%m/%Y")
IN_28_DAYS = (now + dt.timedelta(days=28)).strftime("%d/%m/%Y")


class FlightSearch:
    def __init__(self, sheet_data):
        self.data = sheet_data
        self.flight_info = {}

    def check_iata_codes(self):
        for row_data in self.data:
            tequila_location_params = {"term": row_data["city"]}
            response = requests.get(url=TEQUILA_LOCATIONS_ENDPOINT, params=tequila_location_params, headers=HEADER)
            response.raise_for_status()
            row_data["iataCode"] = response.json()["locations"][0]["code"]

    def get_available_flights(self):
        for row_data in self.data:
            stop_over = True
            flight_stop_over = 0
            while stop_over:
                tequila_search_params = {
                        "fly_from": LOCATION_IATA_CODE,
                        "fly_to": row_data["iataCode"],
                        "date_from": TOMORROW,
                        "date_to": IN_6_MONTHS,
                        "nights_in_dst_from": IN_7_DAYS,
                        "nights_in_dst_to": IN_28_DAYS,
                        "flight_type": "round",
                        "curr": CURRENCY,
                        "one_for_city": 1,
                        "max_stopovers": flight_stop_over,
                            }
                response = requests.get(url=TEQUILA_SEARCH_ENDPOINT, params=tequila_search_params, headers=HEADER)
                response.raise_for_status()
                try:
                    data = response.json()["data"][0]
                    print(f"{row_data['iataCode']} {data['price']}")
                    stop_over = False
                except IndexError:
                    flight_stop_over += 1
                    if flight_stop_over == 2:
                        stop_over = False
                        print(f"No flights found for {row_data['iataCode']}.")
                else:
                    price = data["price"]
                    departure_city = data["route"][0]["cityFrom"]
                    departure_airport = data["route"][0]["flyFrom"]
                    arrival_city = data["route"][0]["cityTo"]
                    arrival_airport = data["route"][0]["flyTo"]
                    inbound_date = data["route"][0]["local_departure"].split("T")[0]
                    outbound_date = data["route"][1]["local_departure"].split("T")[0]
                    flight_data = FlightData(price=price,
                                             departure_city=departure_city,
                                             departure_airport=departure_airport,
                                             arrival_city=arrival_city,
                                             arrival_airport=arrival_airport,
                                             inbound_date=inbound_date,
                                             outbound_date=outbound_date)
                    if flight_stop_over > 0:
                        price = data["price"]
                        departure_city = data["route"][0]["cityFrom"]
                        departure_airport = data["route"][0]["flyFrom"]
                        arrival_city = data["route"][1]["cityTo"]
                        arrival_airport = data["route"][1]["flyTo"]
                        inbound_date = data["route"][0]["local_departure"].split("T")[0]
                        outbound_date = data["route"][2]["local_departure"].split("T")[0]
                        flight_data = FlightData(price=price,
                                                 departure_city=departure_city,
                                                 departure_airport=departure_airport,
                                                 arrival_city=arrival_city,
                                                 arrival_airport=arrival_airport,
                                                 inbound_date=inbound_date,
                                                 outbound_date=outbound_date,
                                                 stop_overs=flight_stop_over,
                                                 via_city=data["route"][0]["cityTo"])
                    self.flight_info[row_data["iataCode"]] = flight_data
