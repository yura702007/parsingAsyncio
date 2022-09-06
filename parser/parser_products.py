import asyncio
from parser_index_page import Parser
from config_parser import URL, TITLES


class ParserProducts(Parser):
    base_url = URL
    titles = TITLES

    def __init__(self, url, title):
        super().__init__(url)
        self.title = title

    def __repr__(self):
        return self.title

    async def run(self):
        print(f'{self.title} is called')


async def main():
    p = Parser()
    task_0 = p.run()
    urls = await asyncio.create_task(task_0)
    tasks = []
    for url, title in urls:
        pp = ParserProducts(url=url, title=title)
        task = await asyncio.create_task(pp.run())
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
