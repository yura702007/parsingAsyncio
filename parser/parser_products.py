import asyncio
import csv
import logging
import logging.config
from pathlib import Path
from datetime import date
from parser_index_page import Parser, urls
from config_parser import URL, TITLES
from bs4 import BeautifulSoup
import time

logging.config.fileConfig('logging.conf')


class ParserProducts(Parser):
    base_url = URL
    titles = TITLES

    def __init__(self, category_name, url, rubric_name):
        super().__init__(url)
        self.category_name = category_name
        self.rubric_name = rubric_name
        self.path = None

    async def run(self):
        await self.create_category_dir()
        await self.create_file()
        while self.url:
            print(self.url)
            task = asyncio.create_task(self.create_session())
            _html = await task
            await self.parser_page(html_code=_html)

    async def create_category_dir(self):
        try:
            self.path = Path('..', 'data', f'{date.today()}', f'{self.category_name}')
            self.path.mkdir(parents=True)
        except FileExistsError:
            pass

    async def create_file(self):
        self.path = Path('..', 'data', f'{date.today()}', f'{self.category_name}', f'{self.rubric_name}.csv')
        with open(self.path, 'w', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=self.titles)
            writer.writeheader()

    async def parser_page(self, html_code):
        try:
            lst = []
            soup = BeautifulSoup(html_code, features='lxml')
            next_products = soup.find('a', class_='show_more')
            next_page = soup.find('a', class_='next_page_link')
            self.update_url(a_down=next_products, a_next=next_page)
            product_block = soup.find('div', class_='products_block__wrapper products_4_columns vertical')
            try:
                product_cards = product_block.find_all('div', class_='form_wrapper')
                for card in product_cards:
                    _dict = {'title': None, 'price': None, 'url': None, 'country': None}
                    try:
                        _dict['title'] = card.find('div', class_='title').text.strip()
                        _dict['price'] = card.find('div', class_='price').text.strip()
                        _dict['url'] = card.find('a', class_='fancy_ajax').get('href').strip()
                        _dict['country'] = card.find('div', class_='small_country').text.strip()
                    except AttributeError as exc:
                        logging.warning(exc, exc_info=True)
                        pass
                    finally:
                        lst.append(_dict)
            except AttributeError as exc:
                logging.warning(exc, exc_info=True)
                return
            await self.write_file(list_product=lst)
        except TypeError as exc:
            logging.error(f'{exc}, {self.url}', exc_info=True)

    async def write_file(self, list_product):
        with open(self.path, 'a', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=self.titles)
            for row in list_product:
                writer.writerow(row)

    def update_url(self, a_down, a_next):
        if a_down:
            self.url = self.base_url + a_down.get('href')
        elif a_next:
            self.url = self.base_url + a_next.get('href')
        else:
            self.url = None


async def main():
    tasks = []
    for category, rubrics in urls.items():
        for url_, rubric in rubrics:
            tasks.append(await ParserProducts(category_name=category, url=url_, rubric_name=rubric).run())
    await asyncio.gather(asyncio.to_thread(*tasks), return_exceptions=True)


if __name__ == '__main__':
    start = time.strftime('%X')
    print('start', start)
    asyncio.run(main())
    end_run = time.strftime('%X')
    print('end', end_run)
    print(f"{start} - {end_run}")
