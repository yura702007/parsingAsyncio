import asyncio
from bs4 import BeautifulSoup
from get_response import create_session


class Parser:

    def __init__(self, url, title):
        self.url = url
        self.title = title

    async def get_html(self):
        task = asyncio.create_task(create_session(url=self.url))
        html_code = await asyncio.gather(task)
        return html_code

    async def run(self):
        result = await self.get_html()
        print(result)


if __name__ == '__main__':
    from parser_index_page import links
    # for _title, _url in links:
    #     print(Parser(url=_url, title=_title))
    _title, _url = next(links)
    p = Parser(title=_title, url=_url)
    asyncio.run(p.run())

