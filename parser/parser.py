import asyncio
from bs4 import BeautifulSoup


class Parser:

    def __init__(self, url, title):
        self.url = url
        self.title = title

    def run(self):
        pass

    def __repr__(self):
        return self.title


if __name__ == '__main__':
    from parser_index_page import links
    for _title, _url in links:
        print(Parser(url=_url, title=_title))

