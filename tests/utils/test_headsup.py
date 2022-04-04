from unittest.mock import patch

import pytest

from ...app.utils.weather import get_headsup_wording

LAT = 14.3
LOT = -175


# TODO: 극단적인 값 케이스 테스트
class TestHeadsUp:
    @pytest.mark.parametrize(
        "wording,pre_weathers",
        [
            (
                "내일 폭설이 내릴 수도 있으니 외출 시 주의하세요.",
                ["snow", "rain", "sun" "snow"],
            ),
            (
                "눈이 내릴 예정이니 외출 시 주의하세요.",
                ["rain", "sun", "rain", "sun", "snow", "rain", "sun" "snow"],
            ),
            (
                "폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요.",
                ["snow", "rain", "sun" "rain"],
            ),
            (
                "며칠동안 비 소식이 있어요.",
                ["snow", "rain", "sun" "sun", "snow", "sun", "sun" "rain"],
            ),
        ],
    )
    @patch("weather.get_weather_data")
    def test_get_headsup(self, mock_get_weather_data, wording, pre_weathers) -> None:
        mock_get_weather_data.retuen_value = pre_weathers
        return_value = get_headsup_wording()
        assert return_value == wording
