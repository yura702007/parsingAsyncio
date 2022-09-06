import asyncio
import re
from datetime import date
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from pathlib import Path
from config_parser import URL, HEADERS


class Parser:
    headers = HEADERS

    def __init__(self, url=URL):
        self.url = url
        self.path = None

    async def run(self):
        self.create_dir()
        task = asyncio.create_task(self.parse_page())
        result = await task
        return result

    def create_dir(self):
        try:
            self.path = Path('..', 'data', f'{date.today()}')
            self.path.mkdir(parents=True)
        except FileExistsError:
            pass

    async def create_session(self):
        async with ClientSession() as session:
            async with session.get(url=self.url, headers=self.headers) as resp:
                try:
                    assert resp.status == 200
                    return await resp.text()
                except AssertionError:
                    return

    async def parse_page(self):
        links = []
        html_code = await self.create_session()
        soup = BeautifulSoup(html_code, features='lxml')
        list_menu = soup.find_all('li', class_='level_1')
        tuple_links = (
            elem.find('a', href=re.compile('/catalog/'), class_=False, text=True) for elem in list_menu
        )
        my_exceptions = ('Тематические подборки', 'Акции', 'Уцененные товары', 'Карты лояльности, сувениры')
        for link in tuple_links:
            try:
                if link.text not in my_exceptions:
                    links.append((link.get('href'), link.text))
            except AttributeError:
                continue
        return links


urls = asyncio.run(Parser().run())


def main():
    for url, title in urls:
        print(url, title)


if __name__ == '__main__':
    main()
