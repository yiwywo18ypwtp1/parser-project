from bs4 import BeautifulSoup
import requests

import asyncio
import aiohttp

from asgiref.sync import sync_to_async

from load_django import *
from parser_app.models import Member, Result

""""
Проход по сссылками и собирание полной информации
"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
}

MAX_CONCURRENT_REQUESTS = 30

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def fetch(session, url):
    try:
        async with semaphore:
            async with session.get(url, headers=HEADERS, timeout=30) as response:
                if response.status == 200:
                    print(f'страница загружена: {url}')
                    return await response.text()
                else:
                    print(f'ошибка загрузки страницы: {url} — статус {response.status}')
    except asyncio.TimeoutError:
        print(f'\n\nтаймаут: {url}\n\n')
    except aiohttp.ClientError as e:
        print(f'ошибка aiohttp: {url} — {e}')
    return None


async def get_member(session, result):
    url = result.link
    html = await fetch(session, url)

    if not html:
        return

    soup = BeautifulSoup(html, 'html.parser')
    profile = {}

    # MMAIN INFORMATION
    try:
        profile['full_name'] = soup.find('span', class_='name').text
    except (AttributeError, AssertionError):
        profile['full_name'] = None

    try:
        profile['license_number'] = soup.find(string="License Number:").find_next('span').text
    except (AttributeError, AssertionError):
        profile['license_number'] = None

    try:
        profile['license_type'] = soup.find(string="License Type:").find_next('span').text
    except (AttributeError, AssertionError):
        profile['license_type'] = None

    try:
        profile['license_status'] = soup.find(string="License Status").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['license_status'] = None

    try:
        profile['eligible_to_practice'] = soup.find(string="Eligible To Practice:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['eligible_to_practice'] = None

    try:
        profile['admit_date'] = soup.find(string="WSBA Admit Date").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['admit_date'] = None

    # Contact Information
    try:
        profile['email'] = soup.find(string="Email:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['email'] = None

    try:
        profile['phone'] = soup.find(string="Phone:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['phone'] = None

    try:
        profile['fax'] = soup.find(string="Fax:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['fax'] = None

    try:
        profile['website'] = soup.find(string="Website:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['website'] = None

    try:
        profile['ttd'] = soup.find(string="TTD:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['ttd'] = None

    # Professional Liability Insurance
    try:
        profile['private_practice'] = soup.find(string="Private Practice:").find('span').text
    except (AttributeError, AssertionError) as e:
        profile['private_practice'] = None

    try:
        profile['is_has_insurance'] = soup.find(string="Has Insurance?").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['is_has_insurance'] = None

    try:
        profile['last_update'] = soup.find(string="Last Updated:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['last_update'] = None

    # Professional Liability Insurance
    try:
        profile['member_of_groups'] = soup.find(string="Member of the following groups:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['member_of_groups'] = None

    try:
        history_table = soup.find('table', class_='history-table')

        history = []
        for row in history_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) == 4:
                group = cells[0].find('span').text.strip()
                position = cells[1].find('span').text.strip()
                start_date = cells[2].find('span').text.strip()
                end_date = cells[3].find('span').text.strip()

                history.append(f"{group}| {position} | {start_date} | {end_date}")

        profile['volunteer_service_history'] = history

    except (AttributeError, AssertionError) as e:
        profile['volunteer_service_history'] = None

    try:
        profile['firm_or_employer'] = soup.find(string="Firm or Employer:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['firm_or_employer'] = None

    try:
        profile['office_type_and_size'] = soup.find(string="Office Type and Size:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['office_type_and_size'] = None

    try:
        profile['practice_areas'] = soup.find(string="Practice Areas:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['practice_areas'] = None

    try:
        profile['languages_other_than_english'] = soup.find(string="Languages Other Than English:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['languages_other_than_english'] = None

    try:
        profile['has_ever_was_as_judge'] = soup.find(string="Has Ever Served as Judge:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['has_ever_was_as_judge'] = None

    for key, value in profile.items():
        print(f'{key}: {value}')

    await save_member_to_db(profile, result)


# Выносим все ORM операции в отдельные sync_to_async функции
@sync_to_async
def save_member_to_db(profile, result):
    try:
        Member.objects.update_or_create(
            license_number=profile['license_number'],
            defaults=profile
        )
        result.status = 'Done'
        result.save()
    except Exception as e:
        print(f"Ошибка сохранения: {e}")


@sync_to_async
def get_all_results():
    return list(Result.objects.filter(status='New'))


async def main():
    all_results = await get_all_results()

    async with aiohttp.ClientSession() as session:
        tasks = [get_member(session, result) for result in all_results]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

