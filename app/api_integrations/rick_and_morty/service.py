from app.api_integrations.rick_and_morty.enums import ResourceType
from app.api_integrations.rick_and_morty.http_client import RickAndMortyHttpClient


class RickAndMortyService:
    def __init__(self, http_client: RickAndMortyHttpClient):
        """
        This layer is designed to encapsulate business logic.
        it can be used to transform source data, validate API responses, etc.
        """
        self._http_client = http_client

    async def get_all(self, *, resource: ResourceType, page: int | None = None, filters: dict | None = None) -> dict:
        if filters is not None:
            params = filters.copy()
        else:
            params = {}

        if page is not None:
            params['page'] = page

        resp = await self._http_client.get(f'/{resource}', params=params)
        return resp.json()

    async def get_single(self, *, resource: ResourceType, resource_id: int) -> dict:
        resp = await self._http_client.get(f'/{resource}/{resource_id}')
        return resp.json()

    async def get_multiple(self, *, resource: ResourceType, resource_ids: list[int]) -> list[dict]:
        path_resource_ids = ','.join(map(str, resource_ids))
        resp = await self._http_client.get(f'/{resource}/{path_resource_ids}')
        return resp.json()
