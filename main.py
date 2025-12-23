import asyncio
import json
from pathlib import Path

from app.api_integrations.rick_and_morty.client import rick_and_morty_client
from app.api_integrations.rick_and_morty.enums import ResourceType
from app.api_integrations.rick_and_morty.service import RickAndMortyService


def _save_json(filename: str, data) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename

    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def _test_all(client: RickAndMortyService, resource: ResourceType, filters: dict) -> None:
    one_page_resource = await client.get_all(resource=resource)
    _save_json(f'one_page_{resource}.json', one_page_resource)

    total_pages = one_page_resource['info']['pages']
    many_pages_resource_tasks = [client.get_all(resource=resource, page=i) for i in range(1, total_pages + 1)]
    many_pages_resource = await asyncio.gather(*many_pages_resource_tasks)
    _save_json(f'many_pages_{resource}.json', many_pages_resource)

    one_page_source_filter = await client.get_all(resource=resource, filters=filters)
    _save_json(f'one_page_{resource}_filter.json', one_page_source_filter)


async def _test_single(client: RickAndMortyService, resource: ResourceType, resource_id: int) -> None:
    single_resource = await client.get_single(resource=resource, resource_id=resource_id)
    _save_json(f'single_{resource}.json', single_resource)


async def _test_multiple(client: RickAndMortyService, resource: ResourceType, resource_ids: list[int]) -> None:
    multiple_resource = await client.get_multiple(resource=resource, resource_ids=resource_ids)
    _save_json(f'multiple_{resource}.json', multiple_resource)


async def main() -> None:
    async with rick_and_morty_client() as client:
        tasks = [
            _test_all(client, ResourceType.CHARACTER, {'status': 'alive'}),
            _test_all(client, ResourceType.LOCATION, {'type': 'Dimension'}),
            _test_all(client, ResourceType.EPISODE, {'name': 'Pilot'}),
            _test_single(client, ResourceType.CHARACTER, 1),
            _test_single(client, ResourceType.LOCATION, 1),
            _test_single(client, ResourceType.EPISODE, 1),
            _test_multiple(client, ResourceType.CHARACTER, [1, 2, 3]),
            _test_multiple(client, ResourceType.LOCATION, [1, 2, 3]),
            _test_multiple(client, ResourceType.EPISODE, [1, 2, 3]),
        ]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    OUTPUT_DIR = Path('output')
    asyncio.run(main())
