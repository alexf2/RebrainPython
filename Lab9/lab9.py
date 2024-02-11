import sys
from operator import itemgetter

from sys_info_utils import MemReportKey, get_current_user_memory_info


def main():
    user_name, memory_total, memory_used, memory_percent = itemgetter(
        MemReportKey.USER, MemReportKey.TOTAL, MemReportKey.USED, MemReportKey.PERCENT,
    )(get_current_user_memory_info())

    print(f'Пользователь: {user_name}\n'
          f'Всего памяти: {memory_total >> 20} MB\n'
          f'Занято памяти: {memory_used >> 20} MB\n'
          f'Процент занятой памяти памяти: {memory_percent} %'
          )


if __name__ == '__main__':
    sys.exit(main())
