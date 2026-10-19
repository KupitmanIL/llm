import requests

URL_EXCHANGE = 'https://api.apilayer.com/fixer/latest'
API_KEY_EXCHANGE = 'wGoLQ1LFtHyZy5nCWxU6ieVbivZ0X6ou'

if not API_KEY_EXCHANGE:
    raise RuntimeError('API_KEY_EXCHANGE not set')

def get_exchange_rate(from_currency,to_currency):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    try:
        resp = requests.get(URL_EXCHANGE, params={'base':from_currency,'symbols':to_currency}, headers={'apikey':API_KEY_EXCHANGE})
    except requests.RequestException:
        return f"Could not reach exchange rate service to check {from_currency} to {to_currency}."
    data = resp.json()
    if resp.status_code != 200 or not data.get('success',True):
        return f"Could not reach exchange rate fot {from_currency} to {to_currency}."

    rate= data.get('rates',{}).get(to_currency)
    if rate is None:
        return f'{to_currency} is not valid currency.'

    return f'One {from_currency} = {rate} {to_currency}'

URL_WEATHER='https://api.weatherapi.com/v1/current.json'
API_KEY_WEATHER='91ab09b113014d9e9ea172907261710'

if not API_KEY_WEATHER:
    raise RuntimeError('API_KEY_WEATHER not set')

def get_weather(city):
    city = city.upper()
    try:
        resp = requests.get(URL_WEATHER,params={'key':API_KEY_WEATHER,'q':city})
    except requests.RequestException:
        return f"Could not reach weather service to check weather in {city}."
    data = resp.json()
    if resp.status_code != 200:
        if data.get('error', {}).get('code') == 1006:
            return f'{city} is not valid city.'
        return f"Could not reach weather service to check weather in {city}."

    weather = data.get('current', {})
    if not weather:
        return f'{city} is not valid city.'
    temperature = weather.get('temp_c')
    condition = weather.get('condition', {}).get('text')
    humidity = weather.get('humidity')
    wind_speed = weather.get('wind_kph')
    city_name = data.get('location', {}).get('name')
    return (
        f"City: {city_name}\n"
        f"Temperature: {temperature}°C\n"
        f"Condition: {condition}\n"
        f"Humidity: {humidity}%\n"
        f"Wind speed: {wind_speed} km/h"
    )
TOOLS = {
    "get_exchange_rate": get_exchange_rate,
    "get_weather": get_weather,
}