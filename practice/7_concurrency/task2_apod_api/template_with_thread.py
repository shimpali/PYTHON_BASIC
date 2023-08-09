import os
import concurrent.futures
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import time

API_KEY = 'snnjwniYYvaFLEdW4arW9WanSQZNAHtagl1LQv0D'
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


def fetch_data(url: str) -> BeautifulSoup:
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request) as response:
        if response.status == 200:
            page = response.read().decode('utf-8')
    return BeautifulSoup(page, 'html.parser')


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    url = f'{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}'
    soup = fetch_data(url)
    data = json.loads(soup.get_text())
    return [item['url'] for item in data if item['media_type'] == 'image']


def download_and_write(url: str, number: int) -> None:
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    path = f'{OUTPUT_IMAGES}/{str(number)}.jpg'
    urllib.request.urlretrieve(url, path)


def download_apod_images(metadata: list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as executor:
        executor.map(download_and_write, metadata, range(len(metadata)))


def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print(time.perf_counter() - start)