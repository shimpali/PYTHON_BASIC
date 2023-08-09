import argparse
import configparser
import json
from unittest.mock import Mock

import pytest
import tempfile
import shutil
from unittest import mock

from main import *
from utils.data_generators import *
from utils.json_handlers import *
from utils.file_handlers import *

config = configparser.ConfigParser()
config.read('test.ini')


# ============= FIXTURES =============
@pytest.fixture()
def mock_args():
    list_of_args = list()
    for section in config.sections():
        list_of_args.append(dict(
            path_to_save_files=config[section]['path_to_save_files'],
            files_count=int(config[section]['files_count']),
            file_prefix=config[section]['file_prefix'],
            file_name=config[section]['file_name'],
            data_lines=int(config[section]['data_lines']),
            multiprocessing=int(config[section]['multiprocessing']),
            clear_path=config[section]['clear_path'],
            data_schema=config[section]['data_schema'],
        ))
    return list_of_args


@pytest.fixture()
def config_data_schemas(mock_args):
    return [args['data_schema'] for args in mock_args]


@pytest.fixture
def mock_directory():
    return tempfile.mkdtemp()


@pytest.fixture
def mock_file_with_json(config_data_schemas):
    file = tempfile.NamedTemporaryFile(delete=False)
    with open(file.name, 'w') as file:
        file.write(json.dumps(config_data_schemas[0]))
    return file


# ============= ARGS HANDLERS =============
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(
                path_to_save_files='./test_output',
                files_count=5,
                file_prefix='count',
                file_name='test_file_name',
                data_lines=100,
                multiprocessing=2,
                data_schema=json.dumps({
                    "date": "timestamp:", "some_int": "int:rand",
                    "type": "int:[1, 2, 3]", "age": "int:rand(1, 90)",
                    "some_str": "str:rand"
                })
            ))
def test_parse_args(default_args):
    assert type(parse_input_args(default_args)) != str


# ============= DATA GENERATORS =============

def test_gen_timestamp():
    timestamp_choices = ['timestamp:', 'tiemstamp:one', 'tiemstamp:two']
    data = [gen_timestamp() for _ in timestamp_choices]
    assert type(data[0]) == float
    assert type(data[1]) == float
    assert type(data[2]) == float


def test_gen_str():
    str_choices = ['rand', "['one', 'two', 'three']", 'abc', '']
    data = [gen_str(value) for value in str_choices]
    regex = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", re.I)
    assert bool(regex.match(data[0])) is True
    assert data[1] in ['one', 'two', 'three']
    assert data[2] == "abc"
    assert data[3] == ''


def test_gen_int():
    int_choices = ['rand', 'rand(10, 20)', '']
    data = [gen_int(value) for value in int_choices]
    assert data[0] in range(0, 100000)
    assert data[1] in range(10, 20)
    assert data[2] is None


# ============= JSON HANDLERS =============
def test_get_data_schema(mock_args):
    for args in mock_args:
        ns = argparse.Namespace(**args)
        data_schema = load_data_schema_from_args(ns)
        assert type(data_schema) != str
        assert 1 < len(data_schema.keys())


def test_get_data_schema_from_file(mock_args, mock_file_with_json):
    mock_schema = mock_args[0]
    print(mock_args[0])
    mock_schema['file_name'] = mock_file_with_json.name
    ns = argparse.Namespace(**mock_schema)
    data_schema = load_data_schema_from_args(ns)
    with open(mock_file_with_json.name, 'r') as file:
        data_from_file = json.load(file)
        assert data_schema == json.loads(data_from_file)
    os.remove(file.name)


# ============= FILE HANDLERS =============s

def validate_uuid(value) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


@pytest.mark.parametrize('correct', ['.', './', os.path.join(os.getcwd(), 'output'), './output'])
@pytest.mark.parametrize('incorrect', ['/Users', '/', '/usr/abc/PycharmProjects/PYTHON-BASIC/practice/Capstone/output'])
def test_check_path(correct, incorrect):
    assert check_path(correct) is True
    assert check_path(incorrect) is False


def test_clear_path(mock_directory):
    file = tempfile.NamedTemporaryFile(dir=mock_directory)
    assert len(os.listdir(mock_directory)) == 1
    file_name = file.name[len(mock_directory) + 1::]
    manage_clear_path(mock_directory, file_name)
    assert os.listdir(mock_directory) == []
    shutil.rmtree(mock_directory)


@pytest.mark.parametrize('number_of_prefixes', [random.randint(1, 10) for _ in range(5)])
def test_create_paths_with_count_prefixes(mock_args, number_of_prefixes):
    for args in mock_args:
        paths = create_paths_with_prefixes(number_of_prefixes, 'count', args['path_to_save_files'], args['file_name'])
        assert len(paths) == number_of_prefixes
        for number, item in enumerate(paths):
            assert int(item[-1]) == number


@pytest.mark.parametrize('number_of_prefixes', [random.randint(1, 10) for _ in range(5)])
def test_create_paths_with_random_prefixes(mock_args, number_of_prefixes):
    for args in mock_args:
        paths = create_paths_with_prefixes(number_of_prefixes, 'random', args['path_to_save_files'], args['file_name'])
        assert len(paths) == number_of_prefixes
        for item in paths:
            assert 0 <= int(item[-1]) < 99999


@pytest.mark.parametrize('number_of_prefixes', [random.randint(1, 10) for _ in range(5)])
def test_create_paths_with_uuid_prefixes(mock_args, number_of_prefixes):
    for args in mock_args:
        paths = create_paths_with_prefixes(number_of_prefixes, 'uuid', args['path_to_save_files'], args['file_name'])
        assert len(paths) == number_of_prefixes
        for item in paths:
            uuid_from_file_name = item.split(f'{args["file_name"]}_')[1]
            assert validate_uuid(uuid_from_file_name) is True


# ============= MAIN =============

def test_generate_data_schema_output(config_data_schemas):
    for index, schema in enumerate(config_data_schemas):
        data_schema = json.loads(schema)
        assert generate_data_schema_output(data_schema, index + 1).keys() == data_schema.keys()


def run_main(args):
    ns = argparse.Namespace(**args)
    if os.path.exists(ns.path_to_save_files):
        shutil.rmtree(ns.path_to_save_files)
    generate_output(ns)
    assert len(os.listdir(ns.path_to_save_files)) == ns.files_count
    shutil.rmtree(ns.path_to_save_files)


def test_single_processing(mock_args):
    single_processes = filter(lambda process: process['multiprocessing'] == 1, mock_args)
    for args in list(single_processes):
        run_main(args)


def test_multi_processing(mock_args):
    multi_processes = filter(lambda process: process['multiprocessing'] > 1, mock_args)
    for args in list(multi_processes):
        run_main(args)
