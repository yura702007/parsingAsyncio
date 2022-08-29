import asyncio
import csv
import time
from datetime import date
from pathlib import Path
from bs4 import BeautifulSoup
from parser_index_page import get_links
from config_parser import TITLES


def save_data(header, gen_data):
    def get_path(title=header):
        dir_name = date.today()
        try:
            path_to_dir = Path('..', 'data_base', f'{dir_name}')
            path_to_dir.mkdir(parents=True)
        except FileExistsError:
            pass
        _path = Path('..', 'data_base', f'{dir_name}', f'{title}.csv')
        return _path

    path = get_path()
    with open(path, 'w', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=TITLES)
        writer.writeheader()
        for row in gen_data:
            writer.writerow(row)


def parser_page(html_code):
    soup = BeautifulSoup(html_code, features='lxml')
    product_block = soup.find('div', class_='products_block__wrapper products_4_columns vertical')
    product_cards = product_block.find_all('div', class_='form_wrapper')
    for card in product_cards:
        try:
            title = card.find('div', class_='title').text.strip()
            price = card.find('div', class_='price').text.strip()
            url = card.find('a', class_='fancy_ajax').get('href').strip()
            country = card.find('div', class_='small_country').text.strip()
            yield {'title': title, 'price': price, 'url': url, 'country': country}
        except AttributeError:
            yield {'title': title, 'price': price, 'url': url, 'country': None}


if __name__ == '__main__':
    start = time.time()
    print(time.time() - start)
