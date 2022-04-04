from pydantic import BaseModel


class Summary(BaseModel):
    greeting: str
    temperature: str
    heads_up: str


class SummaryResponse(BaseModel):
    summary: Summary


class Coordinate(BaseModel):
    lat: float
    lon: float


class CurrentWeatherRequest(Coordinate):
    ...


class CurrentWeatherResponse(BaseModel):
    timestamp: float
    code: int
    temp: float
    rain1h: int


class ForecastWeatherRequest(Coordinate):
    hour_offset: int


class ForecastWeatherResponse(BaseModel):
    timestamp: float
    code: int
    min_temp: float
    max_temp: float
    rain: int


class HistoricalWeatherRequest(Coordinate):
    hour_offset: int


class HistoricalWeatherResponse(BaseModel):
    timestamp: float
    code: int
    temp: float
    rain1h: int
