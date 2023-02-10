import requests
import datetime


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = "x"
        self.locations_endpoint = "https://api.tequila.kiwi.com/locations/query"
        self.search_endpoint = "https://api.tequila.kiwi.com/v2/search"
        self.header = {
            "apikey": self.api_key,
        }
        self.location = "LON"
        self.stop_overs = 1
        self.tomorrow_date = str((datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y"))
        self.six_months_date = str((datetime.date.today() + datetime.timedelta(days=182)).strftime("%d/%m/%Y"))

    def code_finder(self, city) -> str:
        inputs = {
            "term": city,
            "location_types": "city",
        }
        tequila_response = requests.get(
            url=self.locations_endpoint,
            headers=self.header,
            params=inputs
        )
        tequila_response.raise_for_status()
        code = tequila_response.json()["locations"][0]["code"]
        return code

    def flight_finder(self, destination):
        flight_inputs = {
            "fly_from": self.location,
            "fly_to": destination,
            "date_from": self.tomorrow_date,
            "date_to": self.six_months_date,
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "curr": "GBP",
            "max_sector_stopovers": self.stop_overs,
            "vehicle_type": "aircraft",
            "limit": 1,
        }

        search_response = requests.get(
            url=self.search_endpoint,
            headers=self.header,
            params=flight_inputs
        )
        search_response.raise_for_status()
        flights = search_response.json()
        if flights["data"] == "":
            self.stop_overs = 1
            self.flight_finder(destination)
        return flights
