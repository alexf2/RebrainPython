import pprint
import sys
from enum import Enum
from operator import itemgetter
from typing import Final

DT_INDEX = 0
TIME_INDEX = 7
PC_INDEX = 16


class LogField(Enum):
    TIME = 'time'
    COMPUTER = 'pc_name'
    SERVICE = 'service_name'
    MSG = 'message'

    def __repr__(self):
        return self.value


class StorageStatus(Enum):
    OK = 'memory_ok'
    NOT_ENOUGH = 'memory_not_enough'
    CRITICAL = 'memory_critical'

    def __repr__(self):
        return self.value


BYTES_IN_GIGABYTE = 1073741824

FIRST_LIMIT_BYTES = 10 * BYTES_IN_GIGABYTE
FIRST_PERCENT_LIMIT = 5

SECOND_LIMIT_BYTES = 30 * BYTES_IN_GIGABYTE
SECOND_PERCENT_LIMIT = 10


LogsType = Final[tuple[str]]
ParsedList = list[dict[LogField, str]]
StorageReportType = Final[tuple[dict[str, int]]]

LOGS: LogsType = (
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
    'May 24 19:26:40 PC-00102 rtkit-daemon[1131]: Supervising 5 threads of 2 processes of 1 users.',)

STORAGE_REPORT: StorageReportType = (
    {'id': 382, 'total': 999641890816, 'used': 228013805568},
    {'id': 385, 'total': 61686008768, 'used': 52522710872},
    {'id': 398, 'total': 149023482194, 'used': 83612310700},
    {'id': 400, 'total': 498830397039, 'used': 459995976927},
    {'id': 401, 'total': 93386008768, 'used': 65371350065},
    {'id': 402, 'total': 988242468378, 'used': 892424683789},
    {'id': 430, 'total': 49705846287, 'used': 9522710872},
)


def parse_log(log: str) -> dict[LogField, str]:

    service_name_index = log.index(' ', PC_INDEX)
    message_index = log.index(':', service_name_index + 1)

    return {
        LogField.TIME: log[: PC_INDEX - 1],
        LogField.COMPUTER: log[PC_INDEX: service_name_index],
        LogField.SERVICE: log[service_name_index + 1: message_index],
        LogField.MSG: log[message_index + 2:],
    }


def get_parsed_logs(result_list: ParsedList, *logs: str) -> None:
    for log in logs:
        result_list.append(parse_log(log))


def estimate_space(total, used):
    return total - used, round((total - used) / total * 100, 2)


def estimate_status(total, used):
    free_mem_amount, free_mem_percent = estimate_space(total, used)

    if free_mem_amount < FIRST_LIMIT_BYTES or free_mem_percent < FIRST_PERCENT_LIMIT:
        return StorageStatus.CRITICAL
    elif free_mem_amount < SECOND_LIMIT_BYTES or free_mem_percent < SECOND_PERCENT_LIMIT:
        return StorageStatus.NOT_ENOUGH
    else:
        return StorageStatus.OK


def get_disk_statuses(report: StorageReportType) -> dict[StorageStatus, list[int]]:
    result = {}
    getter = itemgetter('id', 'total', 'used')
    for id, total, used in (getter(item) for item in report):
        ids = result.setdefault(estimate_status(total, used), [])
        ids.append(id)

    return result


def main():
    res = []
    # получение словарей логов 1, 2, 4
    get_parsed_logs(res, LOGS[1], LOGS[2], LOGS[4])
    print('Логи: ')
    pprint.pprint(res)

    print('\n' + '-' * 10 + '\n')

    # группировка отчётов дисков по статусам свободного объёма
    storage_statuses = get_disk_statuses(STORAGE_REPORT)
    print('Статусы дисков:')
    pprint.pprint(storage_statuses)


if __name__ == '__main__':
    sys.exit(main())
