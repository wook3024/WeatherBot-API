from unittest.mock import patch

import pytest

from app.utils.weather import Temperature

LAT = 14.3
LOT = -175


# TODO: 15 이하일 때 양수, 음수 케이스 테스트
# TODO: 극단적인 값 케이스 테스트
class TestTemperature:
    @pytest.mark.parametrize(
        "diff_temp_message,cur_temp,pre_temp",
        [
            ("어제보다 n도 더 덥습니다.", 15, 0),
            ("어제보다 n도 덜 춥습니다.", 15, 16),
            ("어제와 비슷하게 덥습니다.", 15, 15),
            ("어제보다 n도 덜 춥습니다.", -2, -3),
            ("어제보다 n도 더 춥습니다.", -2, -1),
            ("어제와 비슷하게 춥습니다.", -2, -2),
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
        print(temps)
        min_max_temp_message = "최고기온은 {}도, 최저기온은 {}도 입니다.".format(
            min(temps), max(temps)
        )
        assert return_value == " ".join([diff_temp_message, min_max_temp_message])
