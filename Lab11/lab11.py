import os
import platform
import socket
import sys

from psutil import virtual_memory


def getpcname():
    n1 = platform.node()
    n2 = socket.gethostname()
    n3 = os.environ['COMPUTERNAME']
    if n1 == n2 or n1 == n3:
        return n1
    elif n2 == n3:
        return n2
    else:
        raise Exception('Computernames are not equal to each other')


class PCMemory:
    def __init__(self, pc_id, user_name, memory_total, memory_used, memory_percent=None):
        self._pc_id = pc_id
        self._user_name = user_name
        if memory_total <= 0:
            raise ValueError(f'memory_total should be a natural non-zero number, but got: {memory_total}')
        self._memory_total = memory_total
        self._memory_used = memory_used
        self._memory_percent = memory_percent

    @property
    def pc_id(self):
        return self._pc_id

    @pc_id.setter
    def pc_id(self, val):
        self._pc_id = val

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val

    @property
    def memory_total(self):
        return self._memory_total

    @memory_total.setter
    def memory_total(self, val):
        self._memory_total = val

    @property
    def memory_used(self):
        return self._memory_used

    @memory_used.setter
    def memory_used(self, val):
        self._memory_used = val

    @property
    def memory_percent(self):
        return self._memory_percent if self._memory_percent is not None else (self._memory_used / self._memory_total)

    def show_used_percent(self):
        print(f'PC with id \'{self.pc_id}\' used {round(self.memory_percent * 100, 2):g} percent of memory')

    @property
    def is_enough_memory(self):
        return 100 - self.memory_percent * 100 >= 10


def main():
    mem_info = virtual_memory()
    pc_mem1 = PCMemory(getpcname(), os.getlogin(), mem_info.total, mem_info.used)
    pc_mem2 = PCMemory(getpcname(), os.getlogin(), mem_info.total, mem_info.used, mem_info.percent / 100)
    pc_mem3 = PCMemory('test1', 'user1', 1000, 250)
    pc_mem4 = PCMemory('test2', 'user2', 1000, 750, 0.24234)
    pc_mem5 = PCMemory('test3', 'user2', 1000, 750)
    pc_mem6 = PCMemory('test4', 'user1', 1000, 910)

    for pc in (pc_mem1, pc_mem2, pc_mem3, pc_mem4, pc_mem5, pc_mem6):
        pc.show_used_percent()
        print(f'is enough = {pc.is_enough_memory}{os.linesep}')


if __name__ == '__main__':
    sys.exit(main())
