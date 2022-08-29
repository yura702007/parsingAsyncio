import asyncio
import re
from pprint import pprint

from aiohttp import ClientSession
from bs4 import BeautifulSoup


class Parser:
    HEADERS = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "X-Amzn-Trace-Id": "Root=1-630084e5-1013eda313f8fa782be2c3b0"
    }
    TITLES = ['title', 'country', 'price', 'url']

    def __init__(self):
        self.url = 'https://e-dostavka.by'
        self.code_index_page = None
        self.urls_list = []
        self.products_page_dict = {}
        self.products_dict = {}

    async def run(self):
        task = asyncio.create_task(self.create_session())
        await task
        self.get_links()

    async def create_session(self, header=None):
        async with ClientSession() as session:
            async with session.get(url=self.url, headers=self.HEADERS) as resp:
                while True:
                    assert resp.status < 400
                    if header:
                        self.products_page_dict[header] = await resp.text()
                        return
                    self.code_index_page = await resp.text()
                    return

    def get_links(self):
        soup = BeautifulSoup(self.code_index_page, features='lxml')
        list_menu = soup.find_all('li', class_='level_1')
        tuple_links = (
            elem.find('a', href=re.compile('/catalog/'), class_=False, text=True) for elem in list_menu
        )
        my_exceptions = ('Тематические подборки', 'Акции')
        for link in tuple_links:
            try:
                if link.text not in my_exceptions:
                    self.urls_list.append((link.text, link.get('href')))
            except AttributeError:
                continue


if __name__ == '__main__':
    parser = Parser()
    asyncio.run(parser.run())
    print(len(parser.urls_list))
