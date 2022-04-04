from unittest.mock import patch

import pytest

from app import cfg
from app.utils.weather import Temperature

LAT = 14.3
LOT = -175


temperature_message = cfg.service.message.temperature


# TODO: 15 이하일 때 양수, 음수 케이스 테스트
# TODO: 극단적인 값 케이스 테스트
class TestTemperature:
    @pytest.mark.parametrize(
        "diff_temp_message,cur_temp,pre_temp",
        [
            (temperature_message.hotter.format(15 - 0), 15, 0),
            (temperature_message.less_hot.format(15 - 16), 15, 16),
            (temperature_message.similarly_hot, 15, 15),
            (temperature_message.less_cold.format(-2 + 3), -2, -3),
            (temperature_message.colder.format(-2 + 1), -2, -1),
            (temperature_message.similarly_cold, -2, -2),
        ],
    )
    @patch("app.utils.weather.Weather.get_weather_data")
    @pytest.mark.asyncio
    async def test_get_temp_message(
        self,
        mock_get_weather_data,
        diff_temp_message: str,
        cur_temp: float,
        pre_temp: float,
    ) -> None:
        temps = [cur_temp, -cur_temp, pre_temp, -pre_temp]
        mock_get_weather_data.return_value = temps
        return_value = await Temperature.get_temp_message(LAT, LOT, cur_temp, pre_temp)
        min_max_temp_message = temperature_message.min_max.format(
            min(temps), max(temps)
        )
        assert return_value == " ".join([diff_temp_message, min_max_temp_message])
