import asyncio
from typing import List
from urllib.parse import urljoin

from httpx import AsyncClient

from .. import cfg, schemas


class Weather(object):
    @staticmethod
    async def request(client, lat, lon, hour_unit, unit_count):
        response = await client.get(
            url=urljoin(
                base=cfg.service.weather.base_url,
                url=cfg.service.weather.historical_endpoint,
            ),
            params={
                "api_key": cfg.service.weather.api_key,
                "lat": lat,
                "lon": lon,
                "hour_offset": hour_unit * unit_count,
            },
        )
        result = response.json()
        return result

    @classmethod
    async def get_weather_data(
        cls,
        lat: float,
        lon: float,
        unit_count: int,
        hour_unit: int,
        hour_offset: int,
        key: str,
    ):
        requests = []
        async with AsyncClient() as client:
            while abs(hour_unit * unit_count) <= abs(hour_offset):
                requests.append(cls.request(client, lat, lon, hour_unit, unit_count))
                unit_count += 1
            results = await asyncio.gather(*requests)

        data_list = []
        for weather in results:
            data = None
            if key == "temp":
                data = weather.get("temp")
            elif key == "weather":
                code = weather.get("code")
                data = cfg.service.weather.weather_map[code]
            data_list.append(data)
        return data_list


class Greeting(object):
    @staticmethod
    async def get_greeting_message(cur_weather: schemas.CurrentWeatherResponse) -> str:
        message = ""
        weather = cfg.service.weather.weather_map[cur_weather.code]
        if weather == "snow":
            message = "눈이 포슬포슬 내립니다."
            if cur_weather.rain1h >= 100:
                message = "폭설이 내리고 있어요."
        elif weather == "rain":
            message = "비가 오고 있습니다."
            if cur_weather.rain1h >= 100:
                message = "폭우가 내리고 있어요."
        elif weather == "smoke":
            message = "날씨가 약간은 칙칙해요."
        elif weather == "sun" and cur_weather.temp >= 30:
            message = "따사로운 햇살을 맞으세요."
        elif cur_weather.temp <= 0:
            message = "날이 참 춥네요."
        else:
            message = "날씨가 참 맑습니다."
        return message


class Temperature(object):
    @staticmethod
    async def get_min_max_temp_message(lat: float, lon: float, hour_offset: int) -> str:
        hour_unit, unit_count = -6, 1
        temps = await Weather.get_weather_data(
            lat=lat,
            lon=lon,
            unit_count=unit_count,
            hour_unit=hour_unit,
            hour_offset=hour_offset,
            key="temp",
        )
        message = "최고기온은 {}도, 최저기온은 {}도 입니다."
        return message.format(min(temps), max(temps))

    @staticmethod
    def get_diff_temp_message(cur_temp: float, pre_temp: float) -> str:
        message = ""
        diff_temp = cur_temp - pre_temp
        if cur_temp >= 15:
            if diff_temp > 0:
                message = "어제보다 n도 더 덥습니다."
            elif diff_temp < 0:
                message = "어제보다 n도 덜 춥습니다."
            else:
                message = "어제와 비슷하게 덥습니다."
        else:
            if diff_temp > 0:
                message = "어제보다 n도 덜 춥습니다."
            elif diff_temp < 0:
                message = "어제보다 n도 더 춥습니다."
            else:
                message = "어제와 비슷하게 춥습니다."

        return message

    @classmethod
    async def get_temp_message(
        cls,
        lat: float,
        lon: float,
        cur_temp: float,
        pre_temp: float,
        hour_offset: int = 24,
    ) -> str:
        diff_temp_message = cls.get_diff_temp_message(
            cur_temp=cur_temp, pre_temp=pre_temp
        )
        min_max_temp_message = await cls.get_min_max_temp_message(
            lat=lat, lon=lon, hour_offset=hour_offset
        )
        return " ".join([diff_temp_message, min_max_temp_message])


class HeadsUp(object):
    @staticmethod
    def check_weather_condition(
        pre_weathers: List,
        hour_offset: int,
        minimum_hour: int,
        cur_weather: str = "snow",
    ) -> bool:
        """Condition check to determine the most appropriate message

        Returns:
            bool: conditional check result
        """
        hour_unit, unit_count = -6, 1
        match_count = sum(
            [
                previous_weather == cur_weather
                for previous_weather in pre_weathers[: abs(hour_offset // hour_unit)]
            ]
        )
        if abs(match_count * hour_unit) >= minimum_hour:
            return True
        return False

    @classmethod
    async def get_headsup_message(cls, lat: float, lon: float) -> str:
        message = ""
        pre_weathers = await Weather.get_weather_data(
            lat=lat,
            lon=lon,
            unit_count=1,
            hour_unit=-6,
            hour_offset=48,
            key="weather",
        )
        if cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=24,
            minimum_hour=12,
            cur_weather="snow",
        ):
            message = "내일 폭설이 내릴 수도 있으니 외출 시 주의하세요."
        elif cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=48,
            minimum_hour=12,
            cur_weather="snow",
        ):
            message = "눈이 내릴 예정이니 외출 시 주의하세요."
        elif cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=24,
            minimum_hour=12,
            cur_weather="rain",
        ):
            message = "폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요."
        elif cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=48,
            minimum_hour=12,
            cur_weather="rain",
        ):
            message = "며칠동안 비 소식이 있어요."
        else:
            message = "날씨는 대체로 평온할 예정이에요."
        return message
