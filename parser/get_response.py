import aiohttp
import asyncio
from parser.config_parser import URL, HEADERS


async def get_response(base_url=URL, link='', headers=HEADERS):
    """
    Принимает url главной страницы, url запрашиваемой страницы и UserAgent
    Возвращает ответ на get-запрос к странице
    :param link: str
    :param base_url: str
    :param headers: dict
    :return: html text
    """
    url = base_url + link
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            assert resp.status < 400
            return resp


async def main():
    task = asyncio.create_task(get_response())
    result = await task
    print(result.status)


if __name__ == '__main__':
    asyncio.run(main())
