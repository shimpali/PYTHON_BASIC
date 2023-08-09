import os
import aiofiles
from bs4 import BeautifulSoup
import json
import time
import aiohttp
import asyncio

API_KEY = 'snnjwniYYvaFLEdW4arW9WanSQZNAHtagl1LQv0D'
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


async def fetch_data(session, url: str):
    async with session.get(url) as response:
        if response.status == 200:
            page = await response.text()
    return BeautifulSoup(page, 'html.parser')


async def get_apod_metadata(session, start_date: str, end_date: str, api_key: str) -> list:
    url = f'{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}'
    soup = await fetch_data(session, url)
    data = json.loads(soup.get_text())
    return [item['url'] for item in data if item['media_type'] == 'image']


async def download_and_write(session, number: int, url: str):
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    async with session.request(method="GET", url=url) as response:
        if response.status == 200:
            image_response = await response.read()

            path = f'{OUTPUT_IMAGES}/{str(number)}.jpg'
            async with aiofiles.open(path, 'wb') as f:
                await f.write(image_response)


async def download_apod_images(session, metadata: list):
    tasks = []
    for index, url in enumerate(metadata):
        tasks.append(asyncio.ensure_future(download_and_write(session, index, url)))

    await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    async with aiohttp.ClientSession() as session:
        metadata = await get_apod_metadata(
            session,
            start_date='2021-08-01',
            end_date='2021-09-30',
            api_key=API_KEY,
        )
        await download_apod_images(session, metadata=metadata)


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    print(time.perf_counter() - start)