from unittest import TestCase
from tools import get_weather


class TestWeatherIntegration(TestCase):

    def setUp(self):
        self.valid_city = "London"
        self.invalid_city = "Abracadabra123456"

    def test_valid_city(self):
        result = get_weather(self.valid_city)

        self.assertIn("City: London", result)
        self.assertIn("Temperature:", result)
        self.assertIn("Condition:", result)
        self.assertIn("Humidity:", result)
        self.assertIn("Wind speed:", result)

    def test_invalid_city(self):
        result = get_weather(self.invalid_city)

        self.assertEqual(
            result,
            f"{self.invalid_city.upper()} is not valid city."
        )