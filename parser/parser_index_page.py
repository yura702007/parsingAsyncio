import re
import time

from bs4 import BeautifulSoup


def get_links(html_code):
    """
    Получает html код главной страницы
    Извлекает из него ссылки на страницы категорий товаров
    :param html_code: str
    :yield: {title: str: url: str}:
    """
    soup = BeautifulSoup(html_code, features='lxml')
    list_menu = soup.find_all('li', class_='level_1')
    tuple_links = (
        elem.find('a', href=re.compile('/catalog/'), class_=False, text=True) for elem in list_menu
    )
    my_exceptions = ('Тематические подборки', 'Акции')
    for link in tuple_links:
        try:
            if link.text not in my_exceptions:
                yield [link.text, link.get('href')]
        except AttributeError:
            continue


async def main():
    start = time.time()
    print(time.time() - start)


if __name__ == '__main__':
    main()
