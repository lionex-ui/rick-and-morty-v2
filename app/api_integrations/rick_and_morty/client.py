from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from httpx import AsyncClient, Limits

from app.api_integrations.rick_and_morty.http_client import RickAndMortyHttpClient
from app.api_integrations.rick_and_morty.service import RickAndMortyService


@asynccontextmanager
async def rick_and_morty_client() -> AsyncGenerator[RickAndMortyService, Any]:
    """
    Generator for secure client management.
    Correct opening/closing of HTTP clients, etc.
    """
    async with AsyncClient(
        base_url="https://rickandmortyapi.com/api",
        timeout=10,
        limits=Limits(
            max_connections=1,
            max_keepalive_connections=1,
        ),
        http2=True,
    ) as http_client:
        yield RickAndMortyService(
            RickAndMortyHttpClient(http_client)
        )
