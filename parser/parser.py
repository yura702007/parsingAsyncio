import asyncio
import time
import csv

from bs4 import BeautifulSoup
from get_response import create_session
from config_parser import URL, TITLES


class Parser:

    def __init__(self, url, title):
        self.url = url
        self.title = title

    async def create_csv_file(self):
        with open(f'{self.title}.csv', 'w', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=TITLES)
            writer.writeheader()

    async def write_csv_file(self, data_dict):
        with open(f'{self.title}.csv', 'a', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=TITLES)
            writer.writerow(data_dict)

    async def get_html(self):
        task = asyncio.create_task(create_session(url=self.url))
        html_code = await asyncio.gather(task)
        return html_code[0]

    async def parse_html(self, html_code):
        soup = BeautifulSoup(html_code, features='lxml')
        cards_div = soup.find('div', class_='products_block__wrapper products_4_columns vertical')
        cards = cards_div.find_all('div', class_='form_wrapper')
        for card in cards:
            _dict = {'title': None, 'url': None, 'price': None, 'country': None}
            try:
                _dict['title'] = card.find('div', class_='title').text.strip()
                _dict['url'] = card.find('a', class_='fancy_ajax').get('href')
                _dict['price'] = ''.join(card.find('div', class_='price').text.strip().split())
                _dict['country'] = card.find('div', class_='small_country').text.strip()
            except AttributeError:
                pass
            finally:
                await self.write_csv_file(_dict)
        if cards_div.find('a', class_='show_more'):
            self.url = URL + cards_div.find('a', class_='show_more').get('href')
        elif cards_div.find('a', class_='next_page'):
            self.url = URL + cards_div.find('a', class_='next_page').get('href')
        else:
            self.url = False

    async def run(self):
        await self.create_csv_file()
        while self.url:
            page = await self.get_html()
            await self.parse_html(page)


if __name__ == '__main__':
    from parser_index_page import links

    # for _title, _url in links:
    #     print(Parser(url=_url, title=_title))
    print('start')
    start = time.time()
    _title, _url = next(links)
    p = Parser(title=_title, url=_url)
    asyncio.run(p.run())
    print(time.time() - start)

"""
<a class="show_more" href="/catalog/8011.html?lazy_steep=2">
            <i class="fa fa-refresh fa-spin">
            </i>
            Загружаю товары...
           </a>
"""
