import asyncio
from typing import List
from urllib.parse import urljoin

from httpx import AsyncClient

from .. import cfg, schemas


class Weather(object):
    @staticmethod
    async def request(
        client: AsyncClient,
        lat: float,
        lon: float,
        hour_unit: int = 0,
        unit_count: int = 0,
        endpoint: str = cfg.service.weather.historical_endpoint,
    ):
        response = await client.get(
            url=urljoin(
                base=cfg.service.weather.base_url,
                url=endpoint,
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
        base_rainfall = cfg.service.weather.base_rainfall
        base_warm_temp = cfg.service.weather.base_warm_temp
        greeting_message = cfg.service.message.greeting
        if weather == "snow":
            message = greeting_message.snow
            if cur_weather.rain1h >= base_rainfall:
                message = greeting_message.heavy_snow
        elif weather == "rain":
            message = greeting_message.rain
            if cur_weather.rain1h >= base_rainfall:
                message = greeting_message.heavy_rain
        elif weather == "foggy":
            message = greeting_message.foggy
        elif weather == "sun" and cur_weather.temp >= base_warm_temp:
            message = greeting_message.sunny
        elif cur_weather.temp <= 0:
            message = greeting_message.cold
        else:
            message = greeting_message.so_clear
        return message


class Temperature(object):
    @staticmethod
    async def get_min_max_temp_message(lat: float, lon: float, hour_offset: int) -> str:
        historical_time_unit = cfg.service.weather.historical_time_unit
        unit_count = 1
        temps = await Weather.get_weather_data(
            lat=lat,
            lon=lon,
            unit_count=unit_count,
            hour_unit=historical_time_unit,
            hour_offset=hour_offset,
            key="temp",
        )
        message = cfg.service.message.temperature.min_max.format(max(temps), min(temps))
        return message

    @staticmethod
    def get_diff_temp_message(cur_temp: float, pre_temp: float) -> str:
        message = ""
        diff_temp = cur_temp - pre_temp
        temperature_message = cfg.service.message.temperature
        if cur_temp >= cfg.service.weather.base_hot_temp:
            if diff_temp > 0:
                message = temperature_message.hotter
            elif diff_temp < 0:
                message = temperature_message.less_hot
            else:
                message = temperature_message.similarly_hot
        else:
            if diff_temp > 0:
                message = temperature_message.less_cold
            elif diff_temp < 0:
                message = temperature_message.colder
            else:
                message = temperature_message.similarly_cold
        return message.format(abs(diff_temp))

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
        historical_time_unit = cfg.service.weather.historical_time_unit
        match_count = sum(
            [
                previous_weather == cur_weather
                for previous_weather in pre_weathers[
                    : abs(hour_offset // historical_time_unit)
                ]
            ]
        )
        if abs(match_count * historical_time_unit) >= minimum_hour:
            return True
        return False

    @classmethod
    async def get_headsup_message(cls, lat: float, lon: float) -> str:
        message = ""
        headsup_message = cfg.service.message.headsup
        historical_time_unit = cfg.service.weather.historical_time_unit
        pre_weathers = await Weather.get_weather_data(
            lat=lat,
            lon=lon,
            unit_count=1,
            hour_unit=historical_time_unit,
            hour_offset=48,
            key="weather",
        )

        if cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=24,
            minimum_hour=12,
            cur_weather="snow",
        ):
            message = headsup_message.heavy_snow
        elif cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=48,
            minimum_hour=12,
            cur_weather="snow",
        ):
            message = headsup_message.snow
        elif cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=24,
            minimum_hour=12,
            cur_weather="rain",
        ):
            message = headsup_message.heavy_rain
        elif cls.check_weather_condition(
            pre_weathers=pre_weathers,
            hour_offset=48,
            minimum_hour=12,
            cur_weather="rain",
        ):
            message = headsup_message.rain
        else:
            message = headsup_message.so_clear
        return message
