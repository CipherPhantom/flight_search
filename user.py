import requests

message = "Welcome to Fortune's Flight Club.\nWe find the best flight deals and email you."
print(message)
first_name = input("What's your first name?\n")
last_name = input("What's your last name?\n")
email = input("What's your email?\n")
email_check = input("Type your email again?\n")

if email_check != email:
    email = input("Type your email again?\n")

users = {
  "user": {
    "firstName": first_name.title(),
    "lastName": last_name.title(),
    "email": email
  }
}

response = requests.post(url=SHEETY_ENDPOINT, json=users)
response.raise_for_status()
