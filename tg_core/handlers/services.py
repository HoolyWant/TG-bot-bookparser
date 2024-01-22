import asyncio
from pprint import pprint
from bs4 import BeautifulSoup

import aiohttp

async def cvs_writer(dict):
    pass


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://books.toscrape.com/catalogue/category/books/travel_2/index.html') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            soup_items = soup.find_all(class_='product_pod')
            soup_list = []
            for item in soup_items:
                title = item.find('h3').text.replace('.', '')
                url = 'https://books.toscrape.com/catalogue/' + item.find_all('a')[0].get('href')[9:]
                upc =
                rewiews_count =
                type =


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
