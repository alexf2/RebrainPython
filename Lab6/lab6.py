import sys
from datetime import datetime
from os import linesep, makedirs, path
from pathlib import Path
from typing import Final

DATE_TIME_FMT = '%b %d %H:%M:%S'
DT_INDEX = 0
TIME_INDEX = 7
PC_INDEX = 16

DATA_PATH = Path('./data/').resolve()
SLICE_FILE_NAME = 'file_6.txt'
SLICE_FILE_PATH = path.join(DATA_PATH, SLICE_FILE_NAME)
ENCODING = 'utf8'
DAY_TO_EXPORT = 20

LogsType = Final[tuple[str]]

LOGS: LogsType = (
    'May 18 11:59:18 PC-00102 plasmashell[1312]: kf.plasma.core: findInCache with a lastModified timestamp of 0 is deprecated',
    'May 18 13:06:54 ideapad kwin_x11[1273]: Qt Quick Layouts: Detected recursive rearrange. Aborting after two iterations.',
    'May 20 09:16:28 PC0078 systemd[1]: Starting PackageKit Daemon...',
    'May 20 11:01:12 PC-00102 PackageKit: daemon start (рус тест)',
    'May 20 12:48:18 PC0078 systemd[1]: Starting Message of the Day...',
    'May 21 14:33:55 PC0078 kernel: [221558.992188] usb 1-4: New USB device found, idVendor=1395, idProduct=0025, bcdDevice= 1.00',
    'May 22 11:48:30 ideapad mtp-probe: checking bus 1, device 3: "/sys/devices/pci0000:00/0000:00:08.1/0000:03:00.3/usb1/1-4"',
    'May 22 11:50:09 ideapad mtp-probe: bus: 1, device: 3 was not an MTP device',
    'May 23 08:06:14 PC-00233 kernel: [221559.381614] usbcore: registered new interface driver snd-usb-audio',
    'May 24 16:19:52 PC-00233 systemd[1116]: Reached target Sound Card.',
    'May 24 19:26:40 PC-00102 rtkit-daemon[1131]: Supervising 5 threads of 2 processes of 1 users.',)


def get_index_by_date_time(logs: LogsType) -> dict[datetime, int]:
    result = list()
    for i, log in enumerate(logs):
        if len(log) < 16:
            continue
        time_stamp = datetime.strptime(str.rstrip(log[:PC_INDEX]), DATE_TIME_FMT)
        result.append((time_stamp, i))

    result.sort(key=lambda item: item[0])

    return result


def main():
    # получаем отсортированный по возрастанию TS индекс пар (TS, index in LOGS)
    indexed_log = get_index_by_date_time(LOGS)
    # ищем минимальную дату с нужным числом
    (_, index) = next(filter(lambda item: item[0].day == DAY_TO_EXPORT, indexed_log), None)

    print(f'Creating {SLICE_FILE_NAME}...')

    # создаём папки для выгрузки файла, если их нет
    makedirs(DATA_PATH, exist_ok=True)
    # пишем строки, Отфильтрованные по дню
    with open(SLICE_FILE_PATH, 'w', encoding=ENCODING) as out_file:
        while index < len(indexed_log) and indexed_log[index][0].day == DAY_TO_EXPORT:
            out_file.write(LOGS[index] + linesep)
            index += 1

    print('File created')

    print('Reading first record time stamp...')
    # проверяем длину, что можно читать то, что нам нужно
    if (path.getsize(SLICE_FILE_PATH)) >= PC_INDEX:
        # открываем наш файл с логом
        with open(SLICE_FILE_PATH, 'r', encoding=ENCODING) as in_file:
            # перескакиваем сразу на время первой записи
            in_file.seek(TIME_INDEX)
            # считываем время
            result = in_file.read(PC_INDEX - TIME_INDEX - 1)

            print(f'First record time on {DAY_TO_EXPORT}th is "{result}"')
    else:
        print('Can\'t read: file is too short')


if __name__ == '__main__':
    sys.exit(main())
