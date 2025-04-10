from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from load_django import *
from parser_app.models import Result

""""
Собираем ссылки на людей с таблицы
"""


base_url = 'https://www.mywsba.org/PersonifyEbusiness/'

for i in range(3305):
    url = f'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&Country=USA&Page={i}'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        print(f'page loaded successfully: {url}')

        search_table = soup.find('table', class_="search-results")


        if search_table:
            for row in search_table.find_all('tr', class_="grid-row"):
                name_cells = row.find_all('td')

                onclick = row.get('onclick', '')
                if onclick:
                    rel_url = onclick.split("'")[1]
                    full_url = urljoin(base_url, rel_url)
                else:
                    full_url = None

                print(f'{full_url}')

                result, created = Result.objects.get_or_create(
                    link=full_url,
                    defaults={
                        'status': 'New',
                        'link': full_url
                    }
                )
                print(f"created: {created} | link: {result.link}")

        else:
            print("table not found")

    else:
        soup = None
        print('page load error')
