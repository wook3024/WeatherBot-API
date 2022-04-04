from typing import Optional

import pytest

from app import cfg, schemas
from app.utils.weather import Greeting

greeting_message = cfg.service.message.greeting


# TODO: 극단적인 값 테스트
class TestGreeting:
    @pytest.mark.parametrize(
        "message,code,rain1h,temp",
        [
            (greeting_message.snow, 3, 99, -1),
            (greeting_message.heavy_snow, 3, 100, -1),
            (greeting_message.rain, 2, 99, -1),
            (greeting_message.heavy_rain, 2, 100, -1),
            (greeting_message.foggy, 1, -1, -1),
            (greeting_message.sunny, 0, -1, 30),
            (greeting_message.cold, 4, -1, 0),
            (greeting_message.clear, 4, -1, 1),
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
