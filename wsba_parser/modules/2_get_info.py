import json

from bs4 import BeautifulSoup
import requests

from load_django import *
from parser_app.models import Member, Result

""""
Проход по сссылками и собирание полной информации
"""


def get_member(url, result):
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
    try:
        profile['private_practice'] = soup.find(string="Private Practice:").find_next('span').text
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

    for key, value in profile.items():
        print(f'{key}: {value}')

    member, created = Member.objects.get_or_create(
        license_number=profile['license_number'],
        defaults={
            'full_name': profile['full_name'],
            'license_number': profile['license_number'],
            'license_type': profile['license_type'],
            'license_status': profile['license_status'],
            'email': profile['email'],
            'phone': profile['phone'],
            'fax': profile['fax'],
            'website': profile['website'],
            'ttd': profile['ttd'],
            'private_practice': profile['private_practice'],
            'is_has_insurance': profile['is_has_insurance'],
            'last_update': profile['last_update'],
            'member_of_groups': profile['member_of_groups'],
        }
    )
    result.status = 'Done'



all_results = Result.objects.filter(status='New')

for result in all_results:
    result_url = result.link
    get_member(result_url, result)
