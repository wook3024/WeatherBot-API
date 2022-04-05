from unittest import mock

import pytest

from app import cfg
from app.utils.weather import Temperature

LAT = 14.3
LOT = -175


temperature_message = cfg.service.message.temperature
base_hot_temp = cfg.service.weather.base_hot_temp
base_cold_temp = cfg.service.weather.base_cold_temp


# TODO: 15 이하일 때 양수, 음수 케이스 테스트
# TODO: 극단적인 값 케이스 테스트
class TestTemperature:
    @pytest.mark.parametrize(
        "diff_temp_message,cur_temp,pre_temp",
        [
            (
                temperature_message.hotter.format(5),
                base_hot_temp,
                base_hot_temp - 5,
            ),
            (
                temperature_message.less_hot.format(1),
                base_hot_temp,
                base_hot_temp + 1,
            ),
            (
                temperature_message.similarly_hot,
                base_hot_temp,
                base_hot_temp,
            ),
            (
                temperature_message.less_cold.format(1),
                base_cold_temp,
                base_cold_temp - 1,
            ),
            (
                temperature_message.colder.format(1),
                base_cold_temp,
                base_cold_temp + 1,
            ),
            (
                temperature_message.similarly_cold,
                base_cold_temp,
                base_cold_temp,
            ),
        ],
    )
    @mock.patch("app.utils.weather.Weather.get_weather_data")
    @pytest.mark.asyncio
    async def test_get_temp_message(
        self,
        mock_get_weather_data: mock.AsyncMock,
        diff_temp_message: str,
        cur_temp: float,
        pre_temp: float,
    ) -> None:
        temps = [cur_temp, -cur_temp, pre_temp, -pre_temp, cur_temp + pre_temp]
        mock_get_weather_data.return_value = temps
        return_value = await Temperature.get_temp_message(LAT, LOT, cur_temp, pre_temp)
        min_max_temp_message = temperature_message.min_max.format(
            max(temps), min(temps)
        )
        assert return_value == " ".join([diff_temp_message, min_max_temp_message])
