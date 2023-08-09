import os
import random
import uuid


def check_path(path_to_save_files: str) -> bool:
    if os.getcwd() in os.path.abspath(path_to_save_files):
        return True
    return False


def manage_clear_path(path_to_save_files: str, file_name: str) -> str:
    try:
        for file in os.listdir(path_to_save_files):
            if file.rstrip().startswith(file_name):
                os.remove(os.path.join(path_to_save_files, file))
                return ''
    except OSError as e:
        return e.strerror


def manage_path(path_to_save_files, clear_path=False, file_name='output_file') -> str:
    try:
        if not check_path(path_to_save_files):
            return 'Path needs to be in a directory...'
        if not os.path.exists(path_to_save_files):
            os.makedirs(path_to_save_files)
        if clear_path == 'True':
            delete_files = manage_clear_path(path_to_save_files, file_name)
            if delete_files:
                return delete_files
    except OSError as e:
        return e.strerror


def create_paths_with_prefixes(number_of_prefixes: int, prefix: str, path_to_save_files: str,
                               file_name: str) -> list:
    if prefix == 'count':
        paths = [str(i) for i in range(number_of_prefixes)]
    elif prefix == 'random':
        paths = random.sample(range(100000), number_of_prefixes)
    elif prefix == 'uuid':
        paths = [str(uuid.uuid4()) for _ in range(number_of_prefixes)]
    else:
        return []
    return [f'{os.path.join(path_to_save_files, file_name)}_{path}' for path in paths]
