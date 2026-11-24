import asyncio

import httpx

from ai_project_skeleton.config import Settings


class AsyncAPIClient:
    def __init__(
        self,
        settings: Settings,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.settings = settings

        headers = {}
        if settings.api_key:
            headers["Authorization"] = f"Bearer {settings.api_key}"

        self.client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.timeout_seconds,
            headers=headers,
            transport=transport,
        )

    async def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await self.client.request(method, path, **kwargs)
                response.raise_for_status()
                return response

            except (
                httpx.TimeoutException,
                httpx.TransportError,
                httpx.HTTPStatusError,
            ) as error:
                retryable = isinstance(
                    error, (httpx.TimeoutException, httpx.TransportError)
                ) or (
                    isinstance(error, httpx.HTTPStatusError)
                    and (
                        error.response.status_code == 429
                        or error.response.status_code >= 500
                    )
                )

                if not retryable or attempt == self.settings.max_retries:
                    raise

                await asyncio.sleep(self.settings.retry_backoff_seconds * (2**attempt))

        raise RuntimeError("Request failed after all retry attempts.")

    async def get(self, path: str, **kwargs) -> httpx.Response:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> httpx.Response:
        return await self.request("POST", path, **kwargs)

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
