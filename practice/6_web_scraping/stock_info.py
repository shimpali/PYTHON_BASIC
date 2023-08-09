"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
from bs4 import BeautifulSoup
import requests
import csv
from typing import List


def request_page(url: str) -> BeautifulSoup:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(response.text, 'html.parser')


def convert_to_int(data_string: str) -> int:
    try:
        return int(data_string)
    except ValueError:
        return 0


def convert_to_float(data_string: str) -> int:
    try:
        return int(''.join(data_string.split(',')))
    except ValueError:
        return 0


def get_company_urls(soup_data: BeautifulSoup) -> list:
    results = soup_data.find(id='scr-res-table')
    company = results.find_all('a')
    return [f'{baseUrl}{element["href"]}' for element in company]


def get_identifier_url(soup: BeautifulSoup, identifier: str) -> str:
    results = soup.find(id='quote-nav')
    profiles = results.find_all('a')
    return \
        [f'{baseUrl}{profile["href"]}' for profile in profiles if identifier in profile['href']][0]


def get_comp_name_and_comp_code(soup: BeautifulSoup) -> tuple:
    data_list = soup.get_text().split(' - ')
    return data_list[0], data_list[1]


def get_profile_data(profile_url: str) -> tuple:
    profile_soup = request_page(profile_url)
    code, name = get_comp_name_and_comp_code(profile_soup.find('h1', 'D(ib) Fz(16px) Lh(18px)'))
    country = str(profile_soup.find('p', 'D(ib) W(47.727%) Pend(40px)')).split('<br/>')[2]
    current = profile_soup.find('p', 'D(ib) Va(t)')
    data_list = current.find_all('span', 'Fw(600)')
    employees = data_list[2].get_text()
    current = profile_soup.find('tbody')
    ceo_info = current.select_one(':nth-child(1)')
    ceo_name = ceo_info.select_one(':nth-child(1)').get_text()
    ceo_year_born = ceo_info.select_one(':nth-child(5)').get_text()
    return name, code, country, employees, ceo_name, ceo_year_born


def get_statistics_data(statistics_url: str) -> tuple:
    statistic_soup = request_page(statistics_url)
    code, name = get_comp_name_and_comp_code(statistic_soup.find('h1', 'D(ib) Fz(16px) Lh(18px)'))
    current = statistic_soup.find('div', 'Fl(end) W(50%) smartphone_W(100%)').find_all('div', 'Pos(r) Mt(10px)')[0]
    week_change = current.find('tbody').find_all('td', "Fw(500) Ta(end) Pstart(10px) Miw(60px)")[1].get_text()
    current = statistic_soup.find('div', 'Fl(start) W(50%) smartphone_W(100%)').find_all('div', 'Pos(r) Mt(10px)')[-2]
    total_cash = current.find('tbody').find_all('td', 'Fw(500) Ta(end) Pstart(10px) Miw(60px)')[0].get_text()
    return name, code, week_change, total_cash


def get_holders_data(holder_url: str) -> tuple:
    def find_blackrock(data_list):
        for element in data_list:
            if 'Blackrock' in str(element):
                return element
        return None

    holder_soup = request_page(holder_url)
    code, name = get_comp_name_and_comp_code(holder_soup.find('h1', 'D(ib) Fz(16px) Lh(18px)'))
    try:
        holder_tab = holder_soup.find('table', 'W(100%) BdB Bdc($seperatorColor)').find('tbody').find_all('tr')
    except AttributeError:
        return name, code, '-', '-', '-', '-'
    try:
        shares, date_reported, out, value = find_blackrock(holder_tab).find_all('td', 'Ta(end) Pstart(10px)')
    except AttributeError:
        return name, code, '-', '-', '-', '-'

    return name, code, shares.get_text(), date_reported.get_text(), out.get_text(), value.get_text()


def get_data_from_companies(company_urls: List[str]) -> tuple[list[tuple], list[tuple], list[tuple]]:
    profiles, statistics, holders = [], [], []
    for company_url in company_urls:
        company_soup = request_page(company_url)
        profile_url = get_identifier_url(company_soup, 'profile')
        statistics_url = get_identifier_url(company_soup, 'statistics')
        holder_url = get_identifier_url(company_soup, 'holders')
        profiles.append(get_profile_data(profile_url))
        statistics.append(get_statistics_data(statistics_url))
        holders.append(get_holders_data(holder_url))

    return profiles, statistics, holders


def create_youngest_ceos_sheet(profiles: list) -> None:
    sorted_profiles = sorted(profiles, key=lambda item: convert_to_int(item[-1]), reverse=True)
    with open('profile.csv', 'w') as profiles_file:
        profiles_file = csv.writer(profiles_file, delimiter=',')
        profiles_file.writerow(['Name', 'Code', 'Country', 'Employees', 'CEO Name', 'CEO Born'])
        profiles_file.writerows(sorted_profiles[:5])


def create_best_week_change_sheet(statistics: list) -> None:
    sorted_statistics = sorted(statistics, key=lambda item: convert_to_float(item[-2].strip('%')), reverse=True)
    with open('statistics.csv', 'w') as statistics_file:
        statistics_file = csv.writer(statistics_file, delimiter=',')
        statistics_file.writerow(['Name', 'Code', 'Week Change', 'Total Cash'])
        statistics_file.writerows(sorted_statistics[:10])


def create_largest_holds_of_blackrock_sheet(holders: list) -> None:
    sorted_holders = sorted(holders, key=lambda item: convert_to_int(item[-1]), reverse=True)
    with open('holders.csv', 'w') as holders_file:
        holders_file = csv.writer(holders_file, delimiter=',')
        holders_file.writerow(['Name', 'Code', 'Shares', 'Date reported', '% Out', 'Value'])
        holders_file.writerows(sorted_holders[:10])


def compose_sheets(url: str):
    initial_request = request_page(url)
    urls = get_company_urls(initial_request)
    profiles, statistics, holders = get_data_from_companies(urls)
    try:
        create_youngest_ceos_sheet(profiles)
        create_best_week_change_sheet(statistics)
        create_largest_holds_of_blackrock_sheet(holders)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    baseUrl = 'https://finance.yahoo.com'
    compose_sheets(f'{baseUrl}/most-active')
