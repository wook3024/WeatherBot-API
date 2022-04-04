import pytest
from fastapi.testclient import TestClient


class TestIndex:
    def test_redirect(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "sleep_time,status_code",
        [
            (1.5, 408),
            (1.3, 200),
        ],
    )
    def test_request_timeout(
        self, client: TestClient, sleep_time: float, status_code: int
    ) -> None:
        response = client.get("/timeout", params={"sleep_time": sleep_time})
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "lat,lon,status_code",
        [
            (2.5, 5.5, 200),
            (None, 200, 400),
        ],
    )
    def test_bad_request(
        self, client: TestClient, lat: float, lon: float, status_code: int
    ) -> None:
        response = client.get("/summary", params={"lon": lon, "lat": lat})
        assert response.status_code == status_code
