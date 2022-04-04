from urllib.parse import urljoin

import httpx
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .. import schemas
from ..utils.weather import get_greeting_wording, get_headsup_wording, get_temp_wording

router = APIRouter()

base_url = "https://thirdparty-weather-api-v2.droom.workers.dev"
current_endpoint = "/current"
api_key = "CMRJW4WT7V3QA5AOIGPBC"


@router.get("/summary", response_model=schemas.SummaryResponse)
async def summary(lon: float, lat: float) -> JSONResponse:
    response = httpx.get(
        url=urljoin(base=base_url, url=current_endpoint),
        params={
            "api_key": api_key,
            "lat": lat,
            "lon": lon,
        },
    )
    cur_weather = response.json()
    greeting_wording = get_greeting_wording(
        schemas.CurrentWeatherResponse(**cur_weather)
    )

    response = httpx.get(
        url=urljoin(base=base_url, url=current_endpoint),
        params={
            "api_key": api_key,
            "lat": lat,
            "lon": lon,
            "hour_offset": -24,
        },
    )
    pre_weather = response.json()
    temp_wording = get_temp_wording(
        lat=lat,
        lon=lon,
        cur_temp=cur_weather.get("temp"),
        pre_temp=pre_weather.get("temp"),
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
