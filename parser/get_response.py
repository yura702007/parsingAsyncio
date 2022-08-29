from pprint import pprint

import aiohttp
import asyncio
from config_parser import URL, HEADERS
from parser_index_page import get_links
from product_page_parser import parser_page


async def create_session(base_url, header=None, headers=HEADERS):
    """
    Принимает url страницы и UserAgent
    Создаёт web-сессию
    Возвращает текст ответа на get-запрос к странице
    :param base_url: str
    :param header: str
    :param headers: dict
    :return: aiohttp.client_reqrep.ClientResponse: response to a request
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, headers=headers) as resp:
            while True:
                assert resp.status < 400
                if header:
                    return {header: await resp.text()}
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
        tasks = []
        for header, link in links:
            task = asyncio.create_task(create_session(header=header, base_url=link))
            tasks.append(task)
        result = await asyncio.gather(*tasks, return_exceptions=True)
        return result
    task = asyncio.create_task(create_session(base_url=base_url))
    result = await task
    return result


async def main():
    html_index_page = await get_response()
    links = get_links(html_index_page)
    html_product_pages = await get_response(links=links)
    pprint(html_product_pages[0])


if __name__ == '__main__':
    asyncio.run(main())
