from unittest.mock import patch

import pytest

from app import cfg
from app.utils.weather import HeadsUp

LAT = 14.3
LON = -175

headsup_message = cfg.service.message.headsup


# TODO: 극단적인 값 케이스 테스트
class TestHeadsUp:
    @pytest.mark.parametrize(
        "message,pre_weathers",
        [
            (
                headsup_message.heavy_snow,
                ["snow", "rain", "sun", "snow"],
            ),
            (
                headsup_message.snow,
                ["rain", "sun", "rain", "sun", "snow", "rain", "sun", "snow"],
            ),
            (
                headsup_message.heavy_rain,
                ["snow", "rain", "sun", "rain"],
            ),
            (
                headsup_message.rain,
                ["sun", "rain", "sun", "sun", "foggy", "sun", "sun", "rain"],
            ),
            (
                headsup_message.clear,
                ["sun", "sun", "sun", "sun", "foggy", "sun", "sun", "rain"],
            ),
        ],
    )
    @patch("app.utils.weather.Weather.get_weather_data")
    @pytest.mark.asyncio
    async def test_get_headsup(
        self, mock_get_weather_data, message, pre_weathers
    ) -> None:
        mock_get_weather_data.return_value = pre_weathers
        return_value = await HeadsUp.get_headsup_message(lat=LAT, lon=LON)
        assert return_value == message
