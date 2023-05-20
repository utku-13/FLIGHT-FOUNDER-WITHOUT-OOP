import os 

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get("TEQAPI")

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/944d0463694aebefe839b2a1e3681b21/flightPrices/sayfa1"

ACCOUNT_SID = os.environ.get("ACCSID")
AUTH_TOKEN = os.environ.get("AUTOK")

TW_NUM = os.environ.get("TWNUM")
MY_NUM = os.environ.get("MYNUM")

import requests
import datetime as dt
from twilio.rest import Client

response = requests.get(url=SHEETY_PRICES_ENDPOINT)
data = response.json()
flights_data = data["sayfa1"]

now = dt.datetime.now()

days_later_60 = now + dt.timedelta(days=60)

current_date = now.strftime("%d/%m/%Y")
date_of_60_days_later = days_later_60.strftime("%d/%m/%Y")

#API KEYLE BU DATAYI YÖNETMEYİ BECERDİK.

location_endpoint = f"{TEQUILA_ENDPOINT}/search"
headers = {"apikey": TEQUILA_API_KEY}
query = {
    "fly_from":"BER",
    "fly_to":"LON",
    #it accepts multiple destination and it can give multiple output .
    "date_from":current_date,
    "date_to":date_of_60_days_later,
    "nights_in_dst_from": 7,
    "nights_in_dst_to": 28,
    "flight_type": "round",
    "one_for_city": 1,
    #for cheapest flight.
    "max_stopovers": 0,
    #it indices direct flight.
    "curr": "EUR"
    #GBP is the code of sterlin . You can alter it with EUR if you would like.
}

response = requests.get(url=location_endpoint, headers=headers, params=query)
data = response.json()["data"][0]["price"]
#it only gives one flight detail BUT
#it is still an element of list so 
#we still need to put [0] after ["data"]

for city_data in flights_data:
    
    query = {
    "fly_from":"LON",
    "fly_to":city_data['iataCode'],
    #it accepts multiple destination and it can give multiple output .
    "date_from":current_date,
    "date_to":date_of_60_days_later,
    "nights_in_dst_from": 7,
    "nights_in_dst_to": 28,
    "flight_type": "round",
    "one_for_city": 1,
    #for cheapest flight.
    "max_stopovers": 0,
    #it indices direct flight.
    "curr": "EUR"
    #GBP is the code of sterlin . You can alter it with EUR if you would like.
    }

    response = requests.get(url=location_endpoint, headers=headers, params=query)
    data = response.json()["data"][0]["price"]
    difference = city_data["lowestPrice"] - data
    print(f"{difference}€ cheaper.")
    lowest_price = city_data["lowestPrice"]
    print(f"cheapest flight:{data}€ ,normal min price:{lowest_price}€ ")
    if city_data["lowestPrice"] > data:
        print("it is way cheaper")
        print(f"exact cost is {data}.") 
        client = Client(ACCOUNT_SID,AUTH_TOKEN)
        message = client.messages \
                    .create(
                        body=f"CHEAP FLIGHT HAS FOUND.\n\nExact cost is {data}.\n It is {difference}€ cheaper. ",
                        from_=TW_NUM,
                        to=MY_NUM,
                    )
    else: 
        print("too expensive.")