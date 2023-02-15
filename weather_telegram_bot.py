"""
Modules:
:module datetime:                       get now date.
:module requests:                       get the JSON result.
:module aiogram.dispatcher.Dispatcher:  process incoming updates.
:module aiogram.utils.excecutor:        start bot in long-pooling mode.
:module aiogram.Bot:                    connect API to execute commands.
:module aiogram.types:                  recognize message type.
:module config:                         is the Open Weather API and the Telegram API tokens.
"""
from datetime import datetime
import requests
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from config import telegram_bot_token, open_weather_token


bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """
    The first greeting, an explanation for user of how to interact with the bot.
    """
    await message.reply('Hello! Please enter the city, the weather which you are interested in.')


@dp.message_handler()
async def get_weather(message: types.Message):
    """
    Gets the name of the city.
    Sends a weather request using the API.
    Sends a response to the user.
    """
    code_to_emoji = {
        'Clear': 'Clear \U00002600',
        'Clouds': 'Clouds \U00002601',
        'Rain': 'Rain \U00002614',
        'Drizzle': 'Rain \U00002614',
        'Thunderstorm': 'Thunderstorm \U000026A1',
        'Snow': 'Snow \U0001F328',
        'Mist': 'Mist \U0001F32B'
    }

    try:
        req = requests.get(
            f'https://api.openweathermap.org/'
            f'data/2.5/weather?q={message.text}&appid={open_weather_token}',
            timeout=5
        )
        data = req.json()

        city = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        now_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        weather_description = data['weather'][0].get('main')

        if weather_description in code_to_emoji:
            weather_emoji = code_to_emoji.get(weather_description)
        else:
            weather_emoji = 'Can`t recognize the weather, please check by yourself.'

        await message.reply(
            f'Weather in <b>{city}</b> on <b>{now_date}</b>,\n'
            f'Current temperature is {round(temp-273.15, 2)}°C, {weather_emoji}\n'
            f'Humidity is {humidity}%,\nPressure is {pressure}hPa,\n'
            f'Wind speed is {wind}m/s',
            parse_mode='HTML'
            )

    except KeyError as ex:
        print(ex)
        await message.reply('Please check city name')

    print(f'{now_date} @{message["from"]["username"]}: {message.text}')


if __name__ == '__main__':
    executor.start_polling(dp)
