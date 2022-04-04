from typing import Optional

import pytest

from app import cfg, schemas
from app.utils.weather import Greeting

greeting_message = cfg.service.message.greeting
base_rainfall = cfg.service.weather.base_rainfall
base_warm_temp = cfg.service.weather.base_warm_temp


# TODO: 극단적인 값 테스트
class TestGreeting:
    @pytest.mark.parametrize(
        "message,code,rain1h,temp",
        [
            (greeting_message.snow, 3, base_rainfall - 1, base_warm_temp - 1),
            (greeting_message.heavy_snow, 3, base_rainfall, base_warm_temp - 1),
            (greeting_message.rain, 2, base_rainfall - 1, base_warm_temp - 1),
            (greeting_message.heavy_rain, 2, 100, base_warm_temp - 1),
            (greeting_message.foggy, 1, base_rainfall - 1, base_warm_temp - 1),
            (greeting_message.sunny, 0, base_rainfall - 1, base_warm_temp),
            (greeting_message.cold, 4, base_rainfall - 1, 0),
            (greeting_message.so_clear, 4, base_rainfall - 1, base_warm_temp - 1),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_greeting_message(
        self,
        message: str,
        code: str,
        rain1h: int,
        temp: float,
    ) -> None:
        return_value = await Greeting.get_greeting_message(
            schemas.CurrentWeatherResponse(
                timestamp=0000000000,
                code=code,
                rain1h=rain1h,
                temp=temp,
            )
        )
        print(
            schemas.CurrentWeatherResponse(
                timestamp=0000000000,
                code=code,
                rain1h=rain1h,
                temp=temp,
            )
        )
        assert message == return_value
