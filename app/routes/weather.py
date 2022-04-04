from typing import Dict, Optional
from urllib.parse import urljoin

import httpx
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .. import cfg, schemas
from ..utils.weather import get_greeting_wording, get_headsup_wording, get_temp_wording

router = APIRouter()


def request_weather_data(
    lon: float,
    lat: float,
    hour_offset: Optional[int] = None,
) -> Dict:
    response = httpx.get(
        url=urljoin(
            base=cfg.service.weather.base_url, url=cfg.service.weather.current_endpoint
        ),
        params={
            "api_key": cfg.service.weather.api_key,
            "lat": lat,
            "lon": lon,
            "hour_offset": hour_offset,
        },
    )
    weather = response.json()
    return weather


@router.get("/summary", response_model=schemas.SummaryResponse)
async def summary(lon: float, lat: float) -> JSONResponse:
    cur_weather = request_weather_data(lon=lon, lat=lat)
    pre_weather = request_weather_data(lon=lon, lat=lat, hour_offset=-24)

    greeting_wording = get_greeting_wording(
        schemas.CurrentWeatherResponse(**cur_weather)
    )
    temp_wording = get_temp_wording(
        lat=lat,
        lon=lon,
        cur_temp=cur_weather.get("temp", float("inf")),
        pre_temp=pre_weather.get("temp", float("inf")),
        hour_offset=-24,
    )
    headsup_wording = get_headsup_wording(lat, lon)
    return JSONResponse(
        content=jsonable_encoder(
            {
                "summary": {
                    "greeting": greeting_wording,
                    "temperature": temp_wording,
                    "heads_up": headsup_wording,
                }
            }
        )
    )
