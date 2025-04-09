from bs4 import BeautifulSoup
import requests

from load_django import *
from parser_app.models import Member, Result

""""
Проход по сссылками и собирание полной информации
"""


def get_member(url, history):
    url = url

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        print('Page loaded successfully')
    else:
        soup = None
        print('Page load error')

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
        profile['public_adress'] = soup.find(string="Public/Mailing Address:").find_next('span').text
    except (AttributeError, AssertionError) as e:
        profile['public_adress'] = None

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
    # try:
    #     private_practice = soup.find(string="Private Practice:")
    #     if private_practice:
    #         profile['private_practice'] = private_practice.find('span').text
    #     else:
    #         profile['private_practice'] = 'NONE'
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

    member, created = Member.objects.get_or_create(
        license_number=profile['license_number'],
        defaults={
            'full_name': profile['full_name'],
            'license_number': profile['license_number'],
            'license_type': profile['license_type'],
            'license_status': profile['license_status'],
            'eligible_to_practice': profile['eligible_to_practice'],
            'admit_date': profile['admit_date'],
            'email': profile['email'],
            'phone': profile['phone'],
            'fax': profile['fax'],
            'website': profile['website'],
            'ttd': profile['ttd'],
            'private_practice': profile['private_practice'],
            'is_has_insurance': profile['is_has_insurance'],
            'last_update': profile['last_update'],
            'member_of_groups': profile['member_of_groups'],
            'volunteer_service_history': profile['volunteer_service_history'],
            'firm_or_employer': profile['firm_or_employer'],
            'office_type_and_size': profile['office_type_and_size'],
            'practice_areas': profile['practice_areas'],
            'languages_other_than_english': profile['languages_other_than_english'],
            'has_ever_was_as_judge': profile['has_ever_was_as_judge'],
        }
    )
    result.status = 'Done'
    result.save()



all_results = Result.objects.filter(status='New')

for result in all_results:
    result_url = result.link
    get_member(result_url, result)
