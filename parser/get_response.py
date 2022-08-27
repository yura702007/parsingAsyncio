import aiohttp
import asyncio
from parser.config_parser import URL, HEADERS


async def create_session(base_url, link, headers=HEADERS):
    """
    Принимает url главной страницы, url запрашиваемой страницы и UserAgent
    Создаёт web-сессию
    Возвращает ответ на get-запрос к странице
    :param link: str
    :param base_url: str
    :param headers: dict
    :return: aiohttp.client_reqrep.ClientResponse: response to a request
    """
    url = base_url + link
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            assert resp.status < 400
            return resp


async def get_response(base_url=URL, link=''):
    """
    Создаёт задачу из корутины create_session
    Возвращает результат
    :param base_url: str
    :param link: str
    :return: aiohttp.client_reqrep.ClientResponse: response to a request
    """
    task = asyncio.create_task(create_session(base_url=base_url, link=link))
    result = await task
    return result


if __name__ == '__main__':
    print(asyncio.run(get_response()).status)
