import csv

from bs4 import BeautifulSoup

import aiohttp


async def cvs_writer(data: list) -> None:
    with open(f'parser.csv', 'w', encoding='utf-8') as file:
        names = ['title', 'url', 'value', 'available', 'upc', 'product_type']
        file_writer = csv.DictWriter(file, delimiter="|",
                                     lineterminator="\r", fieldnames=names)
        file_writer.writeheader()
        for item in data[1:]:
            file_writer.writerow(item)


async def parser(link: str) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
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


async def parser_view(list_: list) -> list:
    async with aiohttp.ClientSession() as session:
        soup_list = [{'category': list_[0]['category'].replace('\n', '')}]
        for dict_ in list_[1:]:
            url = dict_['url']
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                soup_items = soup.find_all(class_='table table-striped')
                for item in soup_items:
                    upc = item.find('td').text
                    product_type = item.find('td').find_next('td').text
                    item_dict = {
                            'upc': upc,
                            'product_type': product_type,
                    }
                    soup_list.append(item_dict)
        return soup_list


async def clear_list(list1: list, list2: list) -> list:
    category = list2[0]['category']
    good_list = [{'category': category}]
    for item in list1[1:]:
        item['upc'] = list2[list1.index(item)]['upc']
        item['product_type'] = list2[list1.index(item)]['product_type']
        good_list.append(item)
    return good_list
