"""
Modules:
:module open_weather_token: is the Open Weather API token.
:module requests:           to get the JSON result.
:module datetime:           to get now date
"""
from datetime import datetime
import requests
from config import open_weather_token
# from pprint import pprint


def get_weather(city, api_token):
    """
    Using the API token and the city entered by the user,
    we return a nice result.

    :param city:                This is the city weather which the user is searching for.
    :param api_token:           Actually, the API token itself
    :return:                    None.
    """
    try:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_token}', timeout=5
        )
        data = req.json()
        # pprint(data)

        city = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']

        print(f'Weather in {city} on {datetime.now().strftime("%d/%m/%Y %H:%M")},\n'
              f'Current temperature is {round(temp-273.15)}°C,\n'
              f'Humidity is {humidity}%,\nPressure is {pressure},\n'
              f'Wind speed is {wind} m/s'
              )

    except KeyError:
        print('Please check city name')


def main():
    """
    The main method that runs everything.

    :return:    None.
    """
    city = input('Enter city name: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
