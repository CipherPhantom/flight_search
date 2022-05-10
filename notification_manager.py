import smtplib
from twilio.rest import Client
from flight_data import FlightData


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def create_alert(self, info: FlightData):
        if info.stop_overs > 0:
            add_alert = f"\nFlight has 1 stop over, via {info.via_city}."
        else:
            add_alert = ""
        alert = f"Only #{info.price} to fly from {info.departure_city}-{info.departure_airport} to " \
                f"{info.arrival_airport}-{info.arrival_airport}, from {info.inbound_date} to {info.outbound_date}."
        alert += add_alert
        return alert

    def send_message(self, alert):
        message = self.client.messages.create(
            body=alert,
            from_="+19379150128",
            to="+2349127676224"
        )
        print(message.status)

    def send_emails(self, alert, users):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            for user in users:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=user["email"],
                    msg=f"Subject:New Low Price Flight!\n\n{alert}".encode("utf-8")
                )
