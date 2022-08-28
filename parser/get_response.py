import aiohttp
import asyncio
from config_parser import URL, HEADERS


async def create_session(base_url, headers=HEADERS):
    """
    Принимает url страницы и UserAgent
    Создаёт web-сессию
    Возвращает текст ответа на get-запрос к странице
    :param base_url: str
    :param headers: dict
    :return: aiohttp.client_reqrep.ClientResponse: response to a request
    """
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(1)
        async with session.get(url=base_url, headers=headers) as resp:
            assert resp.status < 400
            return await resp.text()


async def get_response(base_url=URL, links=None):
    """
    Создаёт задачу из корутины create_session
    Возвращает результат
    :param base_url: str
    :param links: generator
    :return: aiohttp.client_reqrep.ClientResponse: response to a request
    """
    if links:
        tasks = (asyncio.create_task(create_session(list(link.values())[0])) for link in links)
        result = await asyncio.gather(*tasks, return_exceptions=True)
        return result
    task = asyncio.create_task(create_session(base_url=base_url))
    result = await task
    return result


async def main():
    result = await get_response()
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
