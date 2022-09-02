import asyncio
from pprint import pprint

from bs4 import BeautifulSoup
from get_response import create_session


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
            title = card.find('div', class_='title').text.strip()
            url = card.find('a', class_='fancy_ajax').get('href')
            price = ''.join(card.find('div', class_='price').text.strip().split())
            country = card.find('div', class_='small_country').text.strip()
            data.append({'title': title, 'url': url, 'price': price, 'country': country})
        return data

    async def run(self):
        page = await self.get_html()
        result = await self.parse_html(page)
        pprint(result)


if __name__ == '__main__':
    from parser_index_page import links

    # for _title, _url in links:
    #     print(Parser(url=_url, title=_title))
    _title, _url = next(links)
    p = Parser(title=_title, url=_url)
    asyncio.run(p.run())

"""
<a class="show_more" href="/catalog/8011.html?lazy_steep=2">
            <i class="fa fa-refresh fa-spin">
            </i>
            Загружаю товары...
           </a>
"""
