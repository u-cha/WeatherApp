class WeatherAPIError(Exception):
    def __init__(self, message=None):
        self.message = message


class WeatherAPIFailure(WeatherAPIError):
    super().__init__(message="There was a problem on remote API side")


class WeatherAPIRequestError(WeatherAPIError):
    super().__init__(message="There is an issue with your request. Please consult remote API docs")


class WeatherAPIKeyError(WeatherAPIError):
    super().__init__(message="There is an issue with your API key")


class WeatherAPISubscriptionError(WeatherAPIError):
    super().__init__(message="There is subscription error. Please consult remote API terms and conditions")


class WeatherAPIUnknownError(WeatherAPIError):
    super().__init__(message="There was a problem on remote API side")
