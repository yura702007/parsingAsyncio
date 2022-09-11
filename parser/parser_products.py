import asyncio
import csv
from pathlib import Path
from datetime import date
from parser_index_page import Parser, urls
from config_parser import URL, TITLES
from bs4 import BeautifulSoup
import time


class ParserProducts(Parser):
    base_url = URL
    titles = TITLES

    def __init__(self, url, title):
        super().__init__(url)
        self.title = title
        self.path = None

    async def run(self):
        await self.create_file()
        _html = await asyncio.gather(self.create_session(), return_exceptions=True)
        await self.parser_page(html_code=_html[0])

    async def create_file(self):
        self.path = Path('..', 'data', f'{date.today()}', f'{self.title}.csv')
        with open(self.path, 'w', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=self.titles)
            writer.writeheader()

    async def parser_page(self, html_code):
        _dict = {'title': None, 'price': None, 'url': None, 'country': None}
        soup = BeautifulSoup(html_code, features='lxml')
        product_block = soup.find('div', class_='products_block__wrapper products_4_columns vertical')
        product_cards = product_block.find_all('div', class_='form_wrapper')
        for card in product_cards:
            try:
                _dict['title'] = card.find('div', class_='title').text.strip()
                _dict['price'] = card.find('div', class_='price').text.strip()
                _dict['url'] = card.find('a', class_='fancy_ajax').get('href').strip()
                _dict['country'] = card.find('div', class_='small_country').text.strip()
            except AttributeError:
                pass
            finally:
                await self.write_file(dict_product=_dict)

    async def write_file(self, dict_product):
        with open(self.path, 'a', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=self.titles)
            writer.writerow(dict_product)


async def main():
    tasks = []
    for url, title in urls:
        tasks.append(await ParserProducts(url=url, title=title).run())
    await asyncio.gather(asyncio.to_thread(*tasks), return_exceptions=True)


if __name__ == '__main__':
    print('start')
    start = time.strftime('%X')
    asyncio.run(main())
    print(f"{start} - {time.strftime('%X')}")

