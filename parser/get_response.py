from aiohttp import ClientSession
import asyncio
from config_parser import URL, HEADERS


async def create_session(url):
    async with ClientSession() as sessions:
        async with sessions.get(url=url, headers=HEADERS) as resp:
            assert resp.status == 200
            return await resp.text()


async def get_response(url=URL):
    task = asyncio.create_task(create_session(url=url))
    result = await asyncio.gather(task)
    return result


if __name__ == '__main__':
    print(asyncio.run(get_response()))
