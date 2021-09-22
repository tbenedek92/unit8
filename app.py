from flask import Flask, redirect, url_for
import os
from weather import Weather
import geocoder

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/weather/<city>')
def city_weather(city):
    api_key = os.environ.get('OPEN_WEATHER_API_KEY')
    if api_key is not None:
        weather = Weather(api_key=api_key, city=city)
        return f'The temperature in {str(city).title()} is {weather.get_temp_c()} ºC, ' \
               f'which equals to {weather.get_temp_f()} F.'
    else:
        return 'No API key available for connecting to Open Weather'


@app.route('/weather')
def weather_redirect():
    g = geocoder.ip('me')
    return redirect(url_for(f'city_weather', city=g.city))


if __name__ == '__main__':
    app.run(host='0.0.0.0')