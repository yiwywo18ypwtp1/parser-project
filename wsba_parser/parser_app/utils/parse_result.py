import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from parser_app.models import Result
from parser_app.utils import parse_mebmer


base_url = 'https://www.mywsba.org/PersonifyEbusiness/'
url = 'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&Country=USA'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    print('page loaded successfully')
else:
    soup = None
    print('page load error')


def get_results():
    search_table = soup.find('table', class_="search-results")

    if search_table:
        for row in search_table.find_all('tr', class_="grid-row"):
            name_cells = row.find_all('td')
            if len(name_cells) >= 3:
                first_name = name_cells[1].get_text(strip=True)
                last_name = name_cells[2].get_text(strip=True)
                full_name = f"{first_name} {last_name}"

                # тут без чата не обошлось(
                onclick = row.get('onclick', '')
                if onclick:
                    rel_url = onclick.split("'")[1]
                    full_url = urljoin(base_url, rel_url)
                else:
                    full_url = None

                print(f'{full_name} - {full_url}')

                parse_mebmer.get_member(full_url)

                # сейвим в бд
                result = Result(
                    name=full_name,
                    link=full_url
                )
                result.save()
    else:
        print("table not found")


