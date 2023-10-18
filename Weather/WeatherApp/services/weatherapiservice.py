from datetime import datetime, timezone

from decouple import config
import requests

from .weathermapper import WeatherMapper
from ..models import Location
from .weatherapiexceptions import WeatherAPIFailure, WeatherAPIKeyError, WeatherAPIRequestError, \
    WeatherAPISubscriptionError, WeatherAPIUnknownError, WeatherAPIError
from ..models import Weather


class WeatherAPIResponse:
    def __init__(self, error_message=None, payload=None):
        self.error_message = error_message
        self.payload = payload


class WeatherAPIService:
    __API_KEY = config("OPEN_WEATHER_API_KEY")
    __API_LOCATION_LIMIT = config("OPEN_WEATHER_API_LOCATION_LIMIT")
    __location_model = Location
    __API_EXCEPTIONS = {
        400: WeatherAPIRequestError,
        401: WeatherAPIKeyError,
        404: WeatherAPIRequestError,
        429: WeatherAPISubscriptionError,
        500: WeatherAPIFailure,
        502: WeatherAPIFailure,
        503: WeatherAPIFailure,
        504: WeatherAPIFailure,

    }

    @classmethod
    def get_locations_by_name(cls, location_name: str) -> WeatherAPIResponse:
        if cls.__validate_location_name(location_name):
            try:
                payload = cls.__get_locations(location_name)
                return WeatherAPIResponse(payload=payload)
            except WeatherAPIError as error:
                return WeatherAPIResponse(error_message=error.message)
        else:
            return WeatherAPIResponse(error_message="Incorrect location name")

    @staticmethod
    def __validate_location_name(location_name):
        return isinstance(location_name, str)

    @classmethod
    def __get_locations(cls, location_name):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={location_name}' \
              f'&limit={cls.__API_LOCATION_LIMIT}&appid={cls.__API_KEY}'
        response = requests.get(url)
        if response.status_code != 200:
            exception = cls.__API_EXCEPTIONS.get(response.status_code, WeatherAPIUnknownError)
            raise exception
        response_json = response.json()
        output = [cls.__map_location_to_model(location, cls.__location_model) for location in response_json]
        return output

    @staticmethod
    def __map_location_to_model(location, model):
        name = location["name"]
        latitude = location["lat"]
        longitude = location["lon"]
        country = location["country"]
        return model(name=name, latitude=latitude, longitude=longitude, country=country, )

    @classmethod
    def __get_weather_from_api(cls, location: Location) -> WeatherAPIResponse:
        try:
            payload = cls.__get_weather(location)
            return WeatherAPIResponse(payload=payload)
        except WeatherAPIError as error:
            return WeatherAPIResponse(error_message=error.message)

    @classmethod
    def __get_weather(cls, location: Location) -> Weather:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}' \
              f'&appid={cls.__API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code != 200:
            exception = cls.__API_EXCEPTIONS.get(response.status_code, WeatherAPIUnknownError)
            raise exception
        response_dict = response.json()
        weather = WeatherMapper.from_dict(response_dict)
        return weather

    @classmethod
    def get_weather_by_location(cls, location):
        try:
            weather = location.weather.latest()
            obtained_at = weather.obtained_at
            now = datetime.now(timezone.utc)
            time_diff = now - obtained_at
            if time_diff.days > 1:
                raise Weather.DoesNotExist
        except Weather.DoesNotExist:
            weather = cls.__get_weather_from_api(location).payload
            weather.location = location
            weather.save()
        return weather
