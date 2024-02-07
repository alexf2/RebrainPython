import re
import sys
from datetime import datetime
from enum import Enum
from typing import Final

DATE_TIME_FMT = '%b %d %H:%M:%S'
TIME_FMT = '%H:%M:%S'
DATE_FMT = '%b %d'


class Keys(Enum):
    FLD_TIME = 'time'
    FLD_COMPUTER = 'pc_name'
    FLD_SERVICE = 'service_name'
    FLD_MSG = 'message'
    FLD_DATE = 'date'


LOGS: Final[list[str]] = [
    'May 18 11:59:18 PC-00102 plasmashell[1312]: kf.plasma.core: findInCache with a lastModified timestamp of 0 is deprecated',
    'May 18 13:06:54 ideapad kwin_x11[1273]: Qt Quick Layouts: Detected recursive rearrange. Aborting after two iterations.',
    'May 20 09:16:28 PC0078 systemd[1]: Starting PackageKit Daemon...',
    'May 20 11:01:12 PC-00102 PackageKit: daemon start',
    'May 20 12:48:18 PC0078 systemd[1]: Starting Message of the Day...',
    'May 21 14:33:55 PC0078 kernel: [221558.992188] usb 1-4: New USB device found, idVendor=1395, idProduct=0025, bcdDevice= 1.00',
    'May 22 11:48:30 ideapad mtp-probe: checking bus 1, device 3: "/sys/devices/pci0000:00/0000:00:08.1/0000:03:00.3/usb1/1-4"',
    'May 22 11:50:09 ideapad mtp-probe: bus: 1, device: 3 was not an MTP device',
    'May 23 08:06:14 PC-00233 kernel: [221559.381614] usbcore: registered new interface driver snd-usb-audio',
    'May 24 16:19:52 PC-00233 systemd[1116]: Reached target Sound Card.',
    'May 24 19:26:40 PC-00102 rtkit-daemon[1131]: Supervising 5 threads of 2 processes of 1 users.',
]


def log_splitter(item: str) -> dict:
    reg = re.compile(
        r'^(?P<date_time>\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
        r'(?P<computer_name>[\w\-\[\]]+)(:+|\s+)*'
        r'(?P<service_name>[\w\.\-[\]]+)(:+|\s+)*(?P<msg>[\W\w]+)$'
    )

    grp = reg.search(item).group

    return {
        Keys.FLD_TIME: grp('date_time'),
        Keys.FLD_COMPUTER: grp('computer_name'),
        Keys.FLD_SERVICE: grp('service_name'),
        Keys.FLD_MSG: grp('msg')
    }


def build_parsed_logs(logs):
    if not isinstance(logs, list) or len(logs) < 1:
        return []
    return [log_splitter(item) for item in logs]


def split_time(logs_dics):
    if not isinstance(logs_dics, list) or len(logs_dics) < 1:
        return logs_dics

    current_year = datetime.now().year
    for item_dict in logs_dics:
        date_time = datetime.strptime(
            item_dict[Keys.FLD_TIME], DATE_TIME_FMT).replace(year=current_year)

        item_dict[Keys.FLD_TIME] = date_time.time().strftime(TIME_FMT)
        item_dict[Keys.FLD_DATE] = date_time.date().strftime(DATE_FMT)


def to_dic(lst, start_key):
    return {k: value for k, value in enumerate(lst, start_key)}


def main():
    # Создайте из него список словарей, используя ключи из того же задания. Напоминаю
    list_dict_of_logs = build_parsed_logs(LOGS)

    # Выведите на экран список значений <дата/время> всех словарей. Воспользуйтесь списковым включением.
    print([log_dic[Keys.FLD_TIME] for log_dic in list_dict_of_logs])
    # Измените словари в списке: создайте новый ключ 'date', перенеся в его значение дату из поля 'time'. В поле 'time' оставьте только время. Выведите значения для поля 'time' всех словарей в списке.
    split_time(list_dict_of_logs)

    print('-' * 20)

    print([(log_dic[Keys.FLD_TIME], log_dic[Keys.FLD_DATE])
          for log_dic in list_dict_of_logs])

    print('-' * 20)

    # Выведите список значений поля 'message' для всех логов, которые записал ПК с именем 'PC0078'. Воспользуйтесь списковым включением.
    for line in [f'{i}. {log_item[Keys.FLD_MSG]}' for i, log_item in
                 enumerate([log_item for log_item in list_dict_of_logs if log_item[Keys.FLD_COMPUTER] == 'PC0078'], 1)]:
        print(line)

    print('-' * 20)

    # Превратите список словарей логов (который вы сделали в пункте 2) в словарь. Ключами в нем будут целые числа от 100 до 110, а значениями - словари логов.
    dic_of_dics = to_dic(list_dict_of_logs, 100)
    # Выведите на экран словарь лога под ключом 104
    print(dic_of_dics[104])

    return 0


if __name__ == '__main__':
    sys.exit(main())
