import configparser
import logging
import multiprocessing
import sys
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

from utils.args_handlers import *
from utils.json_handlers import *
from utils.data_generators import *
from utils.file_handlers import *

# logging.basicConfig(filename='example.log', level='INFO', format='[%(levelname)s] %(process)d %(filename)s -- %('
#                                                                  'message)s')
logging.basicConfig(level='INFO', format='[%(levelname)s] %(process)d %(filename)s: %(''message)s')
logger = logging.getLogger('magic-generator')


def generate_data_schema_output(data, line_num) -> dict:
    logger.info(f'Generating data_schema {line_num + 1 or ""}')
    output_data_structure = dict()
    data_types: list[str] = ['timestamp', 'int', 'str']
    for key, value in data.items():
        try:
            left, right = value.split(':', 2)
            if left in data_types:
                if left == data_types[0]:
                    if right:
                        logger.warning(f'Timestamp does not support any values. The value {right} will be ignored!')
                    output_data_structure[key] = gen_timestamp()
                if left == data_types[1]:
                    data_int = gen_int(right)
                    if type(data_int) == str:
                        logger.error(data_int)
                        # sys.exit(1)
                    else:
                        output_data_structure[key] = data_int
                elif left == data_types[2]:
                    data_str = gen_str(right)
                    if data_str.find('Wrong') != -1:
                        logger.error(data_str)
                        sys.exit(1)
                    else:
                        output_data_structure[key] = data_str
            else:
                logger.error('Wrong type of data')
                sys.exit(1)
        except ValueError:
            logger.error('Wrong type of data. All values should support special notation “type:what_to_generate”.')
            sys.exit(1)
    return output_data_structure


def generate_multiline_data(data_schema: dict, number_of_lines: int) -> List[Dict]:
    return [generate_data_schema_output(data_schema, line_num) for line_num in range(number_of_lines)]


def manage_multi_processing(number_of_processes, data_schema, data_lines, files_count) -> List[Dict]:
    with multiprocessing.Pool(processes=min(os.cpu_count(), number_of_processes)) as pool:
        data = pool.starmap(partial(generate_multiline_data, data_schema=data_schema, number_of_lines=data_lines),
                            [() for _ in range(files_count)])
    return data


def manage_multi_threading(paths: list, data) -> None:
    with ThreadPoolExecutor(max_workers=min(os.cpu_count() + 4, 32)) as executor:
        executor.map(dump_data_to_json_file, paths, data)


def generate_console_output(data_schema, data_lines) -> None:
    data = generate_multiline_data(data_schema, data_lines)
    if data:
        logger.info('Printing output to console directly as files_count = 0')
        for i in range(len(data)):
            print(json.dumps(data[i]))


def generate_files(args, data_schema):
    if args.clear_path == 'True':
        logger.info('Clearing path...')

    create_path_error = manage_path(args.path_to_save_files, args.clear_path, args.file_name)
    if create_path_error:
        logger.error('Unable to create file/s...')
        logger.error(create_path_error)
        sys.exit(1)
    else:
        logger.info('Creating output directory...')
        multi_processed_data = manage_multi_processing(args.multiprocessing, data_schema, args.data_lines,
                                                       args.files_count)

        if args.file_prefix:
            paths = create_paths_with_prefixes(args.files_count, args.file_prefix,
                                               args.path_to_save_files,
                                               args.file_name)
            if len(paths):
                logger.info('Creating files with data...')
                manage_multi_threading(paths, multi_processed_data)
            else:
                logger.error('Please add one of these prefixes - [\'count\', \'random\', \'uuid\']')
                sys.exit(1)
        else:
            logger.info('Creating a single file as there is no file_prefix...')
            path = os.path.join(args.path_to_save_files, args.file_name)
            dump_data_to_json_file(path, multi_processed_data[0])


def generate_output(args) -> None:
    data_schema = load_data_schema_from_args(args)
    if type(data_schema) == str:
        logger.error(data_schema)
        sys.exit(1)
    else:
        logger.info('Generating data...')
        if args.files_count == 0:
            generate_console_output(data_schema, args.data_lines)
        else:
            generate_files(args, data_schema)
    logger.info('Data Generation successful, application exiting...')


def main() -> None:
    config = configparser.ConfigParser()
    config.read('default.ini')
    args = parse_input_args(config)
    if type(args) == str:
        logger.error(args)
        sys.exit(1)
    else:
        generate_output(args)


if __name__ == '__main__':
    start = time.perf_counter()
    logger.info('Application started...')
    main()
    print(time.perf_counter() - start)
