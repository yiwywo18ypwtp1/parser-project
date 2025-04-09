from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from load_django import *
from parser_app.models import AgencyResult

""""
Собираем ссылки на на агенции со списка
"""

base_url = 'https://www.trovacasa.it'

for i in range(1):
    url = f'https://www.trovacasa.it/agenzie-immobiliari/roma?page={i}'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        print(f'page loaded successfully: {url}')

        agency_cards = soup.find_all('div', class_='listingAgenzie__container')

        if agency_cards:
            for agency in agency_cards:
                href = agency.find(class_='cardAgenzia__logo').find_next('a').get('href')
                url = base_url + href
                print(url)

                result, created = AgencyResult.objects.get_or_create(
                    link=url,
                    defaults={
                        'status': 'New',
                        'link': url
                    }
                )
                print(f"created: {created} | link: {result.link}")

            else:
                print('cards not found')

    else:
        soup = None
        print('page load error')
