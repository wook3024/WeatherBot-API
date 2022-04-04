from unittest.mock import patch

import pytest

from app.utils.weather import HeadsUp

LAT = 14.3
LON = -175


# TODO: 극단적인 값 케이스 테스트
class TestHeadsUp:
    @pytest.mark.parametrize(
        "wording,pre_weathers",
        [
            (
                "내일 폭설이 내릴 수도 있으니 외출 시 주의하세요.",
                ["snow", "rain", "sun", "snow"],
            ),
            (
                "눈이 내릴 예정이니 외출 시 주의하세요.",
                ["rain", "sun", "rain", "sun", "snow", "rain", "sun", "snow"],
            ),
            (
                "폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요.",
                ["snow", "rain", "sun", "rain"],
            ),
            (
                "며칠동안 비 소식이 있어요.",
                ["sun", "rain", "sun", "sun", "smoke", "sun", "sun", "rain"],
            ),
            (
                "날씨는 대체로 평온할 예정이에요.",
                ["sun", "sun", "sun", "sun", "smoke", "sun", "sun", "rain"],
            ),
        ],
    )
    @patch("app.utils.weather.Weather.get_weather_data")
    @pytest.mark.asyncio
    async def test_get_headsup(
        self, mock_get_weather_data, wording, pre_weathers
    ) -> None:
        mock_get_weather_data.return_value = pre_weathers
        return_value = await HeadsUp.get_headsup_wording(lat=LAT, lon=LON)
        assert return_value == wording
