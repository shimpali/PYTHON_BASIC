import argparse
from argparse import Namespace


def validate_args(args) -> str:
    if args.files_count > 1 and not args.file_prefix:
        return 'file_prefix argument needs to be provided if more than 1 file needs to be generated'
    if args.data_lines < 1:
        return 'Number of data lines must be at least 1'
    if args.multiprocessing < 1:
        return 'Number of processes must be at least 1'
    if args.files_count < 0:
        return 'Number of files cannot be negative.'


def parse_input_args(config, default_name='default_values') -> Namespace | str:
    args = argparse.ArgumentParser(prog='magic_generator', description='A console utility for generating test data '
                                                                       'based on the provided data schema')
    args.add_argument('--path_to_save_files',
                      help='Where all files need to save',
                      type=str,
                      default=config.get(default_name, 'path_to_save_files'))
    args.add_argument('--files_count',
                      help='How much json files to generate',
                      type=int,
                      default=config.get(default_name, 'files_count'))
    args.add_argument('--file_name',
                      help='Base file_name. If there is no prefix, the final file name will be file_name.json.'
                           'With prefix full file name will be file_name_file_prefix.json',
                      type=str,
                      default=config.get(default_name, 'file_name'))
    args.add_argument('--file_prefix',
                      help='What prefix for file name to use if more than 1 file needs to be generated',
                      type=str,
                      choices=['count', 'random', 'uuid'],
                      default=config.get(default_name, 'file_prefix')
                      )
    args.add_argument('--data_schema',
                      help='It’s a string with json schema. It could be loaded in two ways: 1) With path to '
                           'json file with schema 2) with schema entered to command line.',
                      default=config.get(default_name, 'data_schema'))
    args.add_argument('--data_lines',
                      help='Count of lines for each file.\n Default, for example: 1000.',
                      type=int,
                      default=config.get(default_name, 'data_lines'))
    args.add_argument('--clear_path',
                      help='If this flag is on, before the script starts creating new data files,'
                           'all files in path_to_save_files that match file_name will be deleted.',
                      default=config.get(default_name, 'clear_path'),
                      action='store_true')
    args.add_argument('--multiprocessing',
                      help='The number of processes used to create files.'
                           'Divides the “files_count” value equally and starts N processes to create an equal'
                           'number of files in parallel.',
                      type=int,
                      default=config.get(default_name, 'multiprocessing'))

    error_in_args = validate_args(args.parse_args())
    if error_in_args is not None:
        return error_in_args
    else:
        return args.parse_args()
