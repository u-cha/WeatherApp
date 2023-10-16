class WeatherAPIError(Exception):
    def __init__(self, message=None):
        self.message = message


class WeatherAPIFailure(WeatherAPIError):
    def __init__(self, message="There was a problem on remote API side"):
        self.message = message


class WeatherAPIRequestError(WeatherAPIError):
    def __init__(self, message="There is an issue with your request. Please consult remote API docs"):
        self.message = message


class WeatherAPIKeyError(WeatherAPIError):
    def __init__(self, message="There is an issue with your API key"):
        self.message = message


class WeatherAPISubscriptionError(WeatherAPIError):
    def __init__(self, message="There is subscription error. Please consult remote API terms and conditions"):
        self.message = message


class WeatherAPIUnknownError(WeatherAPIError):
    def __init__(self, message="There was a problem on remote API side"):
        self.message = message
