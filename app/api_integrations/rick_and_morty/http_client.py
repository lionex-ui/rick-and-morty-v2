from httpx import AsyncClient, Response


class RickAndMortyHttpClient:
    def __init__(self, requests_client: AsyncClient):
        """
        This layer is designed to encapsulate network logic.
        It can be used for additional authorization, logging network requests, etc.
        """
        self._requests_client = requests_client

    async def get(self, endpoint: str, params: dict | None = None) -> Response:
        resp = await self._requests_client.get(endpoint, params=params)
        resp.raise_for_status()
        return resp
