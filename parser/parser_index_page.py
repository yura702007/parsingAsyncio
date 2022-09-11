import asyncio
from datetime import date
from pprint import pprint

from bs4 import BeautifulSoup
from aiohttp import ClientSession
from pathlib import Path
from config_parser import HEADERS


class Parser:
    headers = HEADERS

    def __init__(self, url='https://e-dostavka.by/catalog/'):
        self.url = url
        self.path = None

    async def run(self):
        self.create_dir()
        task = asyncio.create_task(self.pars_page())
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

    async def pars_page(self):
        _html = await self.create_session()
        soup = BeautifulSoup(_html, 'lxml')
        block = soup.find('div', class_='rubrics_table clearfix')
        catalog = block.find_all('div')
        my_exception = ('Уцененные товары', 'Карты лояльности, сувениры', 'Шеф-онлайн')
        category_dict = {}
        for category in catalog:
            links = []
            rubrics = category.find_all('div', class_='item')
            if rubrics:
                if category.find('div', class_='title').text in my_exception:
                    continue
                category_name = category.find('div', class_='title').text
                for rubric in rubrics:
                    a = rubric.find('a')
                    links.append((a.get('href'), a.text))
                category_dict[category_name] = links
        return category_dict


urls = asyncio.run(Parser().run())


def main():
    for key, value in urls.items():
        print(key)
        pprint(value)
        print()


if __name__ == '__main__':
    main()
