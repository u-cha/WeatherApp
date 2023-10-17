from ..models import Weather


class WeatherMapper:
    @staticmethod
    def from_dict(weather_dict: dict) -> Weather:
        try:
            short_type = weather_dict["weather"][0]["main"]
            temperature = weather_dict["main"]["temp"]
            description = weather_dict["weather"][0]["description"]
        except KeyError:
            raise KeyError(f"Incorrect input: weather_dict does not contain necessary keys")
        return Weather(short_type=short_type, temperature=temperature, description=description)
