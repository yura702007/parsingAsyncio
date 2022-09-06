import asyncio
import csv
from pathlib import Path
from datetime import date
from parser_index_page import Parser, urls
from config_parser import URL, TITLES


class ParserProducts(Parser):
    base_url = URL
    titles = TITLES

    def __init__(self, url, title):
        super().__init__(url)
        self.title = title

    async def run(self):
        await self.create_file()
        await self.create_session()

    async def create_file(self):
        path = Path('..', 'data', f'{date.today()}', f'{self.title}.csv')
        with open(path, 'w', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=self.titles)
            writer.writeheader()


async def main():
    tasks = []
    for url, title in urls:
        p = ParserProducts(url=url, title=title)
        task = asyncio.create_task(p.run())
        tasks.append(task)
    for t in tasks:
        await t


if __name__ == '__main__':
    asyncio.run(main())
