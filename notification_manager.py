from flight_data import FlightData
from twilio.rest import Client
import smtplib


class NotificationManager(FlightData):
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        super().__init__()
        self.ACCT_SID = "x"
        self.AUTH_TOKEN = "x"
        self.TWILIO_NUM = "x"
        self.MY_NUM = "x"
        self.password = "x"
        self.my_gmail = "x"

    def send_text(self):
        if len(self.cheaper_list) > 0:
            for dictionary in self.cheaper_list:
                client = Client(self.ACCT_SID, self.AUTH_TOKEN)
                message = client.messages \
                    .create(
                            body=f"Low price alert! Only £{dictionary['price']} to fly from "
                                 f"{dictionary['airport_from']} to {dictionary['airport_to']}{dictionary['via_city']}, "
                                 f"from {dictionary['date_from']} to {dictionary['date_to']}.",
                            from_="x",
                            to="x"
                    )
                print(message.status)

    def send_email(self):
        self.ask_emails()
        users_list = self.get_emails()["users"]
        for account in users_list:
            first_name = account["firstName"]
            user_email = account["email"]

            if len(self.cheaper_list) > 0:
                for dictionary in self.cheaper_list:
                    text = (f"Dear {first_name},\n\nLow price alert!\nOnly £{dictionary['price']} to fly from "
                            f"{dictionary['airport_from']} to {dictionary['airport_to']}{dictionary['via_city']}, "
                            f"from {dictionary['date_from']} to {dictionary['date_to']}.\n\n{dictionary['link']}")\

                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=self.my_gmail, password=self.password)
                        connection.sendmail(
                            from_addr=self.my_gmail,
                            to_addrs=user_email,
                            msg=f"Subject: New Low Price Flight!\n\n{text}".encode('utf-8')
                        )
