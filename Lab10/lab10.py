import logging
import os
import sys
import time

logging.basicConfig(
    filename='./log_file.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%b %d %H:%M:%S',
    level=logging.INFO)


def parce_args(count, delay):
    if not str.isnumeric(count):
        raise TypeError(f'"count" should be an integer, but got {count}')
    result_count = int(count)
    if 0 > result_count or result_count > len(os.environ):
        raise ValueError('count should be in range 0 - 100')

    if not str.replace(delay, '.', '').isnumeric():
        raise TypeError(f'"delay" should be a number, but got {delay}')
    result_delay = float(delay)
    if result_delay < 0.1 or result_delay > 60:
        raise ValueError('"delay" should be in range 0.1 - 60 seconds')

    return result_count, result_delay


def main(args):
    if len(args) != 3:
        print('Needs two args: "count" and "delay"')
        return -1

    count = ...
    delay = ...
    try:
        count, delay = parce_args(args[1], args[2])
    except Exception as err:
        print(str(err))
        return -1

    i = 0
    env_vars_iterator = iter(os.environ.copy().items())
    while i < count:
        time.sleep(delay)
        key, value = next(env_vars_iterator)
        logging.info(f'{key} --> {value}')
        i += 1

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
