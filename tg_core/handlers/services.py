import asyncio

from bs4 import BeautifulSoup

import aiohttp


async def cvs_writer(data):
    category = data[0]['category']
    with open(f'{category}.csv', 'a', encoding='utf-8') as file:
        for item in data:




async def parser(link: str) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            soup_items = soup.find_all(class_='product_pod')
            category = soup.find(class_='page-header action').text
            soup_list = [{'category': category}]
            for item in soup_items:
                title = item.find('h3').text.replace('.', '')
                url = 'https://books.toscrape.com/catalogue/' + item.find_all('a')[0].get('href')[9:]
                value = item.find(class_='product_price').find('p').text
                available = item.find(class_='instock availability').text.replace(' ', '').replace('\n', '')
                item_dict = {
                    'title': title,
                    'url': url,
                    'value': value,
                    'available': available,
                    'upc': '',
                    'product_type': '',
                }
                soup_list.append(item_dict)
            return soup_list


async def parser_view(list_) -> list:
    for dict_ in list_[1:]:
        url = dict_['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                soup_items = soup.find_all(class_='table table-striped')
                soup_list = []
                for item in soup_items:
                    upc = item.find('td').text
                    product_type = item.find('td').find_next('td').text
                    item_dict = {
                        'upc': upc,
                        'product_type': product_type,
                    }
                    soup_list.append(item_dict)
    return soup_list


def clear_list(list1: list, list2: list) -> list:
    good_list = []
    for item in list1:
        item['upc'] = list2[list1.index(item) + 1]['upc']
        item['product_type'] = list2[list1.index(item)]['product_type']
        good_list.append(item)
    return good_list


loop = asyncio.get_event_loop()
loop.run_until_complete(parser_view('https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html'))
