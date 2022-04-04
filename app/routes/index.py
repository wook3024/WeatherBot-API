import asyncio

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """Redirect to docs page

    Returns:
        RedirectResponse: Docs html
    """
    return RedirectResponse(url="/docs")


@router.get("/livez")
async def livez() -> PlainTextResponse:
    """Health check for Dev API server.
    Make sure it works with Kubernetes liveness probe

    Returns:
        sPlainTextResponse: Health check response
    """
    return PlainTextResponse("\n", status_code=200)


@router.get("/timeout", include_in_schema=False)
async def route_for_test(sleep_time: float) -> None:
    await asyncio.sleep(sleep_time)
