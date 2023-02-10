from flight_search import FlightSearch
import requests


class DataManager(FlightSearch):
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        super().__init__()
        self.sheet_endpoint_prices = "https://api.sheety.co/x/flightDeals/prices"
        self.sheet_endpoint_users = "https://api.sheety.co/x/flightDeals/users"

        self.inputs = {
            "price": {

            }
        }

        self.sheet_response = requests.get(
            url=self.sheet_endpoint_prices,
            json=self.inputs,
            auth=("x", "x")
        )
        self.sheet_response.raise_for_status()
        self.prices = self.sheet_response.json()["prices"]

        self.cities_list = [item["city"] for item in self.prices]

        self.row = 2
        self.flight_list = []

        for city in self.cities_list:
            iata = self.code_finder(city)

            inputs = {
                "price": {
                    "iataCode": iata
                }
            }

            sheet_response = requests.put(
                url=f"{self.sheet_endpoint_prices}/{self.row}",
                json=inputs,
                auth=("x", "x")
            )
            sheet_response.raise_for_status()
            self.row += 1
            self.flight_list.append(self.flight_finder(iata)["data"])

        self.sheet_table = requests.get(url=self.sheet_endpoint_prices, auth=("x", "x"))
        self.sheet_table.raise_for_status()
        self.travel_table = self.sheet_table.json()

    def ask_emails(self):
        def email_checker():
            email = input("What is your email?\n")
            email_check = input("Repeat your email:\n")

            if email == email_check:
                print("Welcome to the flight club!")
            else:
                print("Emails don't match. Try again.")
                email = email_checker()
            return email

        print(
            "Welcome to Barney's Flight Club.\nWe find the best flight deals and email them to you."
        )
        first_name = input("What is your first name?\n")
        last_name = input("What is your last name?\n")
        user_email = email_checker()

        inputs = {
            "user": {
                "firstName": first_name.capitalize(),
                "lastName": last_name.capitalize(),
                "email": user_email,
            }
        }

        sheety_response = requests.post(url=self.sheet_endpoint_users, auth=("x", "x"), json=inputs)
        sheety_response.raise_for_status()

    def get_emails(self):
        sheety_users_response = requests.get(
            url=self.sheet_endpoint_users,
            auth=("x", "x"),
            json=self.inputs
        )
        sheety_users_response.raise_for_status()
        users_table = sheety_users_response.json()
        return users_table
