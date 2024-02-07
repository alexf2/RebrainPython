import sys


BYTES_IN_GIGABYTE = 1073741824

FIRST_LIMIT_BYTES = 10 * BYTES_IN_GIGABYTE
FIRST_PERCENT_LIMIT = 5

SECOND_LIMIT_BYTES = 30 * BYTES_IN_GIGABYTE
SECOND_PERCENT_LIMIT = 10

DATA = [
    {'total': 999641890816, 'used': 228013805568},
    {'total': 61686008768, 'used': 52522710872},
    {'total': 149023482194, 'used': 83612310700},
    {'total': 498830397039, 'used': 459995976927},
    {'total': 93386008768, 'used': 65371350065},
    {'total': 988242468378, 'used': 892424683789},
    {'total': 49705846287, 'used': 9522710872},
]


def estimate_space(record):
    return record['total'] - record['used'], round((record['total'] - record['used']) / record['total'] * 100, 2)


def process_input():
    order_num = input(f'Введите номер накопителя до {len(DATA)}> ')
    try:
        order_num = int(order_num)
    except Exception as ex:
        print(f'Ошибка парсинга номера "{
              order_num}": [{str(ex)}], ожидается цело положительное число 1 - {len(DATA)}')
        return -1

    if order_num < 1 or order_num > len(DATA):
        print(f'Ожидается целое положительное число 1 - {len(DATA)}')
        return -2

    free_mem_amount, free_mem_percent = estimate_space(DATA[order_num - 1])

    msg = ...
    if free_mem_amount < FIRST_LIMIT_BYTES or free_mem_percent < FIRST_PERCENT_LIMIT:
        msg = f'На накопителе {order_num} критически мало свободного места'
    elif free_mem_amount < SECOND_LIMIT_BYTES or free_mem_percent < SECOND_PERCENT_LIMIT:
        msg = f'На накопителе {order_num} мало свободного места'
    else:
        msg = f'На накопителе {order_num} достаточно свободного места'

    print(msg)

    return 0


if __name__ == '__main__':
    sys.exit(process_input())
