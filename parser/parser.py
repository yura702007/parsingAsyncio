import asyncio

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


if __name__ == '__main__':
    parser = Parser()
    asyncio.run(parser.run())
    print(parser.code_index_page)
