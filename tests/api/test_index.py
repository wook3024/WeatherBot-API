from fastapi.testclient import TestClient


class TestIndex:
    def test_redirect(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
