import requests
import json


class Weather:

    def __init__(self, api_key, city):
        self.__city = city
        self.__api_key = api_key
        self.__weather_details = self.__get_weather()

    def get_temp_c(self):
        return self.__weather_details['main']['temp']

    def get_temp_f(self):
        temp_c = self.get_temp_c()
        return round((temp_c * 1.8) + 32, 2)

    def __get_weather(self):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.__city}&appid={self.__api_key}&units=metric'
        response = requests.request("GET", url)

        if response.status_code == 200:
            parsed = json.loads(response.text)
            return parsed
        else:
            raise APIError(response.status_code, response.text)


class APIError(Exception):
    def __init__(self, error_code, msg):
        super().__init__(f'API returned http code: {error_code}', msg)