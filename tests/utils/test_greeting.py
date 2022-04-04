from typing import Optional

import pytest

from app import schemas
from app.utils.weather import Greeting

LAT = 14.3
LOT = -175


# TODO: 극단적인 값 테스트
class TestGreeting:
    @pytest.mark.parametrize(
        "wording,code,rain1h,temp",
        [
            ("눈이 포슬포슬 내립니다.", 3, 99, -1),
            ("폭설이 내리고 있어요.", 3, 100, -1),
            ("비가 오고 있습니다.", 2, 99, -1),
            ("폭우가 내리고 있어요.", 2, 100, -1),
            ("날씨가 약간은 칙칙해요.", 1, -1, -1),
            ("따사로운 햇살을 맞으세요.", 0, -1, 30),
            ("날이 참 춥네요.", 4, -1, 0),
            ("날씨가 참 맑습니다.", 4, -1, 1),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_greeting_wording(
        self,
        wording: str,
        code: str,
        rain1h: int,
        temp: float,
    ) -> None:
        return_value = await Greeting.get_greeting_wording(
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
        assert wording == return_value
