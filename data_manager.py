import requests

class DataManager:
    """This class is responsible for talking to the Google Sheet."""
    def __init__(self):
        self.get_response = requests.get(PRICE_SHEETY_ENDPOINT)

    def get_sheet_data(self):
        self.get_response.raise_for_status()
        return self.get_response.json()["prices"]

    def update_sheet(self, data):
        for row_data in data:
            id_no = row_data.pop("id")
            price_data = {"price": row_data}
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{id_no}", json=price_data)
            response.raise_for_status()

    def get_users_emails(self):
        response = requests.get(url=USERS_SHEETY_ENDPOINT)
        return response.json()["users"]
