from urllib.parse import urljoin

import httpx

from .. import cfg, schemas


def get_greeting_wording(cur_weather: schemas.CurrentWeatherResponse) -> str:
    wording = ""
    weather = cfg.service.weather.weather_map[cur_weather.code]
    if weather == "snow":
        wording = "눈이 포슬포슬 내립니다."
        if cur_weather.rain1h >= 100:
            wording = "폭설이 내리고 있어요."
    elif weather == "rain":
        wording = "비가 오고 있습니다."
        if cur_weather.rain1h >= 100:
            wording = "폭우가 내리고 있어요."
    elif weather == "smoke":
        wording = "날씨가 약간은 칙칙해요."
    elif weather == "sun" and cur_weather.temp >= 30:
        wording = "따사로운 햇살을 맞으세요."
    elif cur_weather.temp <= 0:
        wording = "날이 참 춥네요."
    else:
        wording = "날씨가 참 맑습니다."
    return wording


def get_weather_data(
    lat: float,
    lon: float,
    unit_count: int,
    hour_unit: int,
    hour_offset: int,
    key: str,
):
    results = []
    while abs(hour_unit * unit_count) <= abs(hour_offset):
        response = httpx.get(
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
        previous_weather = response.json()
        data = None
        if key == "temp":
            data = previous_weather.get("temp")
        elif key == "weather":
            code = previous_weather.get("code")
            data = cfg.service.weather.weather_map[code]
        results.append(data)
        unit_count += 1
    return results


def get_min_max_temp_wording(lat: float, lon: float, hour_offset: int) -> str:
    hour_unit, unit_count = -6, 1
    temps = get_weather_data(
        lat=lat,
        lon=lon,
        unit_count=unit_count,
        hour_unit=hour_unit,
        hour_offset=hour_offset,
        key="temp",
    )
    wording = "최고기온은 {}도, 최저기온은 {}도 입니다."
    return wording.format(min(temps), max(temps))


def get_diff_temp_wording(cur_temp: float, pre_temp: float) -> str:
    wording = ""
    diff_temp = cur_temp - pre_temp
    if cur_temp >= 15:
        if diff_temp > 0:
            wording = "어제보다 n도 더 덥습니다."
        elif diff_temp < 0:
            wording = "어제보다 n도 덜 춥습니다."
        else:
            wording = "어제와 비슷하게 덥습니다."
    else:
        if diff_temp > 0:
            wording = "어제보다 n도 덜 춥습니다."
        elif diff_temp < 0:
            wording = "어제보다 n도 더 춥습니다."
        else:
            wording = "어제와 비슷하게 춥습니다."

    return wording


def get_temp_wording(
    lat: float,
    lon: float,
    cur_temp: float,
    pre_temp: float,
    hour_offset: int = 24,
) -> str:
    diff_temp_wording = get_diff_temp_wording(cur_temp=cur_temp, pre_temp=pre_temp)
    min_max_temp_wording = get_min_max_temp_wording(
        lat=lat, lon=lon, hour_offset=hour_offset
    )
    return " ".join([diff_temp_wording, min_max_temp_wording])


def check_weather_condition(
    lat: float,
    lon: float,
    hour_offset: int,
    minimum_hour: int,
    cur_weather: str = "snow",
) -> bool:
    """Condition check to determine the most appropriate wording

    Returns:
        bool: conditional check result
    """
    hour_unit, unit_count = -6, 1
    pre_weathers = get_weather_data(
        lat=lat,
        lon=lon,
        unit_count=unit_count,
        hour_unit=hour_unit,
        hour_offset=hour_offset,
        key="weather",
    )
    match_count = sum(
        [
            previous_weather == cur_weather
            for previous_weather in pre_weathers[: abs(hour_offset // hour_unit)]
        ]
    )
    if abs(match_count * hour_unit) >= minimum_hour:
        return True
    return False


def get_headsup_wording(lat: float, lon: float) -> str:
    wording = ""
    if check_weather_condition(
        lat=lat,
        lon=lon,
        hour_offset=24,
        minimum_hour=12,
        cur_weather="snow",
    ):
        wording = "내일 폭설이 내릴 수도 있으니 외출 시 주의하세요."
    elif check_weather_condition(
        lat=lat,
        lon=lon,
        hour_offset=48,
        minimum_hour=12,
        cur_weather="snow",
    ):
        wording = "눈이 내릴 예정이니 외출 시 주의하세요."
    elif check_weather_condition(
        lat=lat,
        lon=lon,
        hour_offset=24,
        minimum_hour=12,
        cur_weather="rain",
    ):
        wording = "폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요."
    elif check_weather_condition(
        lat=lat,
        lon=lon,
        hour_offset=48,
        minimum_hour=12,
        cur_weather="rain",
    ):
        wording = "며칠동안 비 소식이 있어요."
    else:
        wording = "날씨는 대체로 평온할 예정이에요."
    return wording
