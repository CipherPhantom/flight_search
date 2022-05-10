class FlightData:
    """This class is responsible for structuring the flight data."""
    def __init__(self,
                 price,
                 departure_city,
                 departure_airport,
                 arrival_city,
                 arrival_airport,
                 inbound_date,
                 outbound_date, stop_overs=0, via_city=""):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.arrival_city = arrival_city
        self.arrival_airport = arrival_airport
        self.inbound_date = inbound_date
        self.outbound_date = outbound_date
        self.stop_overs = stop_overs
        self.via_city = via_city
