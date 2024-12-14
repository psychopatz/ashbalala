# utils/http_client.py
import httpx

class HTTPClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    async def post(self, endpoint: str, data=None, json=None, headers=None, files=None):
        response = await self.client.post(
            endpoint, 
            data=data, 
            json=json, 
            headers=headers, 
            files=files
        )
        response.raise_for_status()
        return response

    async def get(self, endpoint: str, params=None, headers=None):
        response = await self.client.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response