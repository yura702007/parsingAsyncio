import asyncio
import time
from pprint import pprint

from bs4 import BeautifulSoup
from get_response import create_session
from config_parser import URL, TITLES


class Parser:

    def __init__(self, url, title):
        self.url = url
        self.title = title

    async def get_html(self):
        task = asyncio.create_task(create_session(url=self.url))
        html_code = await asyncio.gather(task)
        return html_code[0]

    async def parse_html(self, html_code):
        data = []
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
                data.append(_dict)
        show_more = cards_div.find('a', class_='show_more')
        if show_more:
            self.url = URL + show_more.get('href')
        else:
            self.url = False
        return data

    async def run(self):
        result = []
        while self.url:
            page = await self.get_html()
            result.extend(await self.parse_html(page))


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
