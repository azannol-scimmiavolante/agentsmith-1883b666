"""Custom exceptions for WeatherApp."""


class WeatherError(Exception):
    """Exception raised for weather API errors."""

    def __init__(self, message: str, status_code: int = None):
        """Initialize WeatherError.

        Args:
            message: Error message describing what went wrong
            status_code: HTTP status code if applicable
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
