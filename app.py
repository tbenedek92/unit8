from flask import Flask, redirect, url_for
import os
from weather import Weather
import geocoder
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge
import time
import threading

API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/weather/<city>')
def city_weather(city):

    if API_KEY is not None:
        weather = Weather(api_key=API_KEY, city=city)
        return f'The temperature in {str(city).title()} is {weather.get_temp_c()} ºC, ' \
               f'which equals to {weather.get_temp_f()} F.'
    else:
        return 'No API key available for connecting to Open Weather'


@app.route('/weather')
def weather_redirect():
    g = geocoder.ip('me')
    return redirect(url_for(f'city_weather', city=g.city))


def define_weather_metrics(frequency=30):
    city_list = ["Zurich", "Budapest"]
    gauge_dict = {}
    for city in city_list:
        gauge = Gauge(f'{str(city).lower()}_c', f'Current temperature in C in {str(city).title()}')
        gauge_dict[city] = gauge
    while True:
        for city, gauge in gauge_dict.items():
            try:
                weather = Weather(api_key='2c8b9ce56ec6c9c1cb144355157f5c7e', city=city)
                temp=weather.get_temp_c()
                gauge.set(temp)
                print(city, temp)
            except ConnectionError:
                print(f'ConnectionError cannnot update {city}\' temp')
                continue
        time.sleep(frequency)


if __name__ == '__main__':
    print("test msg")
    threading.Thread(target=define_weather_metrics, args=[60]).start()
    app.run(host='0.0.0.0')
