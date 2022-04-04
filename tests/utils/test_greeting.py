from typing import Optional

import pytest

from ...app.utils.weather import get_greeting_wording

LAT = 14.3
LOT = -175


# TODO: 극단적인 값 테스트
class TestGreeting:
    @pytest.mark.parametrize(
        "wording,weather,rain1h,temp",
        [
            ("눈이 포슬포슬 내립니다.", "snow", 99, None),
            ("폭설이 내리고 있어요.", "snow", 100, None),
            ("비가 오고 있습니다.", "rain", 99, None),
            ("폭우가 내리고 있어요.", "rain", 100, None),
            ("날씨가 약간은 칙칙해요.", "smoke", None, None),
            ("따사로운 햇살을 맞으세요.", "sun", None, 30),
            ("날이 참 춥네요.", None, None, 0),
            ("날씨가 참 맑습니다.", None, None, 1),
        ],
    )
    def test_get_greeting_wording(
        self,
        wording: str,
        weather: Optional[str],
        rain1h: Optional[int],
        temp: Optional[float],
    ) -> None:
        return_value = get_greeting_wording(weather, rain1h, temp)
        assert wording == return_value
