import re

from enum import Enum
from typing import Final


class Keys(Enum):
    FLD_DATE = 'date_time'
    FLD_COMPUTER = 'computer_name'
    FLD_SERVICE = 'service_name'
    FLD_MSG = 'msg'


# Скопируйте их к себе и создайте из них список (OK: скопировал и сделал список литералов)
LIST_DATA: Final[list[str]] = [
    'May 18 11:59:18 PC-0102 plasmashell[1312]: kf.plasma.core: findInCache with a lastModified timestamp of 0 is deprecated',
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


def printDic(msg, dic):
    print('\t' + msg +
          ', '.join([f'{key}: {val}' for key, val in dic.items()]))

# Создайте алгоритм заполнения словаря, подходящий для любой строчки лога.
# Словарь должен содержать в себе такую информацию (OK: создал)


def log_splitter(item: str) -> dict:
    reg = re.compile(
        r'^(?P<date_time>\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
        r'(?P<computer_name>[\w\-\[\]]+)(:+|\s+)*'
        r'(?P<service_name>[\w\.\-[\]]+)(:+|\s+)*(?P<msg>[\W\w]+)$'
    )

    grp = reg.search(item).group

    return {
        Keys.FLD_DATE: grp('date_time'),
        Keys.FLD_COMPUTER: grp('computer_name'),
        Keys.FLD_SERVICE: grp('service_name'),
        Keys.FLD_MSG: grp('msg')
    }


def fill(dic: dict, key_name: str) -> dict:
    return {key_name: dic.get(key_name, '')}

# Заполните словарь для одной из строк лога с помощью данного алгоритма,
# запросив у пользователя номер строки с помощью input(). (OK: запросил и заполнил)


def parce_picked_string() -> dict:
    str_n = int(input('string number > '))

    if 1 > str_n or str_n > len(LIST_DATA):
        print(f'Выход за пределы: 1 - {len(LIST_DATA)}')
        return {}
    else:
        str_n -= 1
        print(f'\tИндекс: {str_n}')
        dic = log_splitter(LIST_DATA[str_n])

        return dic


selected_dict = parce_picked_string()
# Выведите на экран информацию из текущего словаря в таком виде: <имя компьютера>: <сообщение> (OK: вывел)
print(f'{selected_dict[Keys.FLD_COMPUTER]} : {
      selected_dict[Keys.FLD_MSG]}')

# Скопируйте к себе литерал списка
test_log_splitted_record = [
    'May 26 12:48:18', 'ideapad', 'systemd[1]', 'Finished Message of the Day.']

# Создайте список ключей из пункта 2.1
test_list_keys = [Keys.FLD_DATE, Keys.FLD_COMPUTER,
                  Keys.FLD_SERVICE, Keys.FLD_MSG]
test_dict = dict(zip(test_list_keys, test_log_splitted_record))

# Используя функцию zip(), создайте словарь из этих двух списков
# Создайте список словарей: из словаря, который вы получили в пункте 2 и словаря из пункта 3
printDic('Выбранный лог: ', selected_dict)
printDic('Тестовый лог: ', test_dict)

# Используя преобразование во множество, выведите список совпадающих значений полученных словарей
'''
print('Совпадающие значения: ')
for key in selected_dict.keys() & test_dict.keys():
    if selected_dict[key] == test_dict[key]:
        print('\t', selected_dict[key])
'''

print('Совпадающие значения: ')
for val in set(selected_dict.values()).intersection(test_dict.values()):
    print(f'\t{val}')
