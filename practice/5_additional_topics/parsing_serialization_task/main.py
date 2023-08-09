import os
import json
from statistics import mean
from typing import Dict
from lxml import etree


def read_json_files(source_path: str) -> Dict[str, any]:
    cities = dict()
    for root, dirs, files in os.walk(source_path):
        if len(files):
            with open(os.path.join(root, files[0])) as json_file:
                text = json.load(json_file)
                cities[root.split('/').pop()] = text['hourly']
    return cities


def parse_hourly_data_for_city(cities_data: dict) -> dict:
    temp = list()
    wind_speed = list()
    for hourly_data in cities_data:
        temp.append(hourly_data['temp'])
        wind_speed.append(hourly_data['wind_speed'])
    return {
        'temp': {
            'mean_temp': round(mean(temp), 2),
            'max_temp': max(temp),
            'min_temp': min(temp)
        },
        'wind_speed': {
            'mean_wind_speed': round(mean(wind_speed), 2),
            'max_wind_speed': max(wind_speed),
            'min_wind_speed': min(wind_speed)
        }
    }


def parse_data_for_country(cities_data: dict) -> dict:
    country_mean_temp = round(mean([all_data['temp']['mean_temp'] for all_data in cities_data.values()]), 2)
    country_mean_wind_speed = round(
        mean([all_data['wind_speed']['mean_wind_speed'] for all_data in cities_data.values()]), 2)
    coldest_place, _ = min(cities_data.items(), key=lambda city: city[1]['temp']['mean_temp'])
    warmest_place, _ = max(cities_data.items(), key=lambda city: city[1]['temp']['mean_temp'])
    windiest_place, _ = max(cities_data.items(), key=lambda city: city[1]['wind_speed']['mean_wind_speed'])

    return {
        'mean_temp': str(country_mean_temp),
        'mean_wind_speed': str(country_mean_wind_speed),
        'coldest_place': coldest_place,
        'warmest_place': warmest_place,
        'windiest_place': windiest_place
    }


def process_weather_data(source_path: str) -> dict:
    cities_data = dict()
    data_from_files = read_json_files(source_path)
    for city_name, city_data in data_from_files.items():
        cities_data[city_name] = parse_hourly_data_for_city(city_data)
    country_data = parse_data_for_country(cities_data)
    return {'cities_data': cities_data, 'country_data': country_data}


def write_to_xml(result_path, summary_data, cities_data) -> None:
    root = etree.Element('weather', country='Spain', date='2021-09-25')
    etree.SubElement(root, 'summary', **summary_data)
    city_element = etree.SubElement(root, 'cities')
    for city, hourly_data in sorted(cities_data.items()):
        city_element.append(
            etree.Element(
                city.strip().replace(' ', '_'),
                mean_temp=str(hourly_data['temp']['mean_temp']),
                max_temp=str(hourly_data['temp']['max_temp']),
                min_temp=str(hourly_data['temp']['min_temp']),
                mean_wind_speed=str(hourly_data['wind_speed']['mean_wind_speed']),
                max_wind_speed=str(hourly_data['wind_speed']['max_wind_speed']),
                min_wind_speed=str(hourly_data['wind_speed']['min_wind_speed'])))
    element_tree = etree.ElementTree(root)
    etree.indent(element_tree, space="\t", level=0)
    with open(result_path, 'wb') as output_file:
        element_tree.write(output_file)


if __name__ == '__main__':
    path = 'source_data'
    parsed_data = process_weather_data(path)
    write_to_xml('weather_results.xml', parsed_data['country_data'], parsed_data['cities_data'])
