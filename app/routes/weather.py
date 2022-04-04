import asyncio
from typing import Dict, Optional
from urllib.parse import urljoin

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient

from .. import cfg, schemas
from ..utils.weather import Greeting, HeadsUp, Temperature

router = APIRouter()


async def request_weather_data(
    client: AsyncClient,
    lon: float,
    lat: float,
    endpoint: str,
    hour_offset: Optional[int] = None,
) -> Dict:
    response = await client.get(
        url=urljoin(
            base=cfg.service.weather.base_url,
            url=endpoint,
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
async def summary(lon: float, lat: float) -> ORJSONResponse:
    async with AsyncClient() as client:
        cur_weather, pre_weather = await asyncio.gather(
            request_weather_data(
                client=client,
                lon=lon,
                lat=lat,
                endpoint=cfg.service.weather.current_endpoint,
            ),
            request_weather_data(
                client=client,
                lon=lon,
                lat=lat,
                endpoint=cfg.service.weather.historical_endpoint,
                hour_offset=-24,
            ),
        )
    greeting_wording, temp_wording, headsup_wording = await asyncio.gather(
        Greeting.get_greeting_wording(schemas.CurrentWeatherResponse(**cur_weather)),
        Temperature.get_temp_wording(
            lat=lat,
            lon=lon,
            cur_temp=cur_weather.get("temp", float("inf")),
            pre_temp=pre_weather.get("temp", float("inf")),
            hour_offset=-24,
        ),
        HeadsUp.get_headsup_wording(lat, lon),
    )
    return ORJSONResponse(
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
