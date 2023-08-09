import os
import queue
import threading
from random import randint
import time
import multiprocessing as mp
from queue import Queue

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1


def convert_list_to_queue(data_list: list) -> Queue:
    """Using queue here as it's thread safe"""

    q = Queue()
    [q.put(i) for i in data_list]
    return q


def write_to_individual_files(q: Queue):
    while True:
        try:
            number, result = q.get(block=False)
        except queue.Empty:
            return
        with open(OUTPUT_DIR + '/' + str(number) + '.txt', 'w') as f:
            f.write(str(result))
        q.task_done()


def calculate_fib(fib_list: list):
    with mp.Pool() as pool:
        fib_data = pool.map(fib, fib_list)
    data = [(fib_list[fib_value], fib_data[fib_value]) for fib_value in range(len(fib_list))]

    task_queue = convert_list_to_queue(data)
    threads = [threading.Thread(target=write_to_individual_files, args=(task_queue,)) for _ in range(min(os.cpu_count() + 4, 32))]
    [t.start() for t in threads]
    task_queue.join()


def read_and_write(result_file: str):
    results_queue = convert_list_to_queue(os.listdir(OUTPUT_DIR))
    results = []

    def read_data():
        while True:
            try:
                path = results_queue.get(block=False)
            except queue.Empty:
                return None
            with open(OUTPUT_DIR + '/' + path, 'r') as f:
                results.append((path.split('.')[0], f.read()))
            results_queue.task_done()

    def write_results_to_csv():
        lock = threading.Lock()
        with lock:
            with open(result_file, 'w') as f:
                for data in results:
                    value, result = sorted(data,  key=lambda item: item, reverse=True)
                    f.write(f'{value},{result}\n')

    threads = [threading.Thread(target=read_data) for _ in range(min(os.cpu_count() + 4, 32))]
    threads.append(threading.Thread(target=write_results_to_csv))
    [t.start() for t in threads]
    results_queue.join()


if __name__ == '__main__':
    start = time.perf_counter()
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    calculate_fib(fib_list=[randint(1, 1000) for _ in range(1000)])
    read_and_write(result_file=RESULT_FILE)
    print(time.perf_counter() - start)
