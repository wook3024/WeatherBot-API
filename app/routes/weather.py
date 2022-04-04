import asyncio

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient

from .. import cfg, logger, schemas
from ..utils.weather import Greeting, HeadsUp, Temperature, Weather

router = APIRouter()


@router.get("/summary", response_model=schemas.SummaryResponse)
async def summary(lon: float, lat: float) -> ORJSONResponse:
    logger.info("Request data \nlon: {}, lat: {}".format(lon, lat))
    async with AsyncClient() as client:
        cur_weather, pre_weather = await asyncio.gather(
            Weather.request(
                client=client,
                lon=lon,
                lat=lat,
                endpoint=cfg.service.weather.current_endpoint,
            ),
            Weather.request(
                client=client,
                lon=lon,
                lat=lat,
                hour_unit=-6,
                unit_count=4,
                endpoint=cfg.service.weather.historical_endpoint,
            ),
        )
    logger.debug("Current weather \n{}".format(cur_weather))
    logger.debug("Previous weather \n{}".format(pre_weather))
    greeting_message, temp_message, headsup_message = await asyncio.gather(
        Greeting.get_greeting_message(schemas.CurrentWeatherResponse(**cur_weather)),
        Temperature.get_temp_message(
            lat=lat,
            lon=lon,
            cur_temp=cur_weather.get("temp"),
            pre_temp=pre_weather.get("temp"),
            hour_offset=-24,
        ),
        HeadsUp.get_headsup_message(lat, lon),
    )
    return ORJSONResponse(
        content=jsonable_encoder(
            {
                "summary": {
                    "greeting": greeting_message,
                    "temperature": temp_message,
                    "heads_up": headsup_message,
                }
            }
        )
    )
