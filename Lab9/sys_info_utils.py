import os
from enum import Enum

from psutil import virtual_memory


class MemReportKey(Enum):
    USER = 'user_name'
    TOTAL = 'memory_total'
    USED = 'memory_used'
    PERCENT = 'memory_percent'


def get_current_user_memory_info() -> dict[MemReportKey, str | int | float]:
    mem_info = virtual_memory()
    return {
        MemReportKey.USER: os.getlogin(),
        MemReportKey.TOTAL: mem_info.total,
        MemReportKey.USED: mem_info.used,
        MemReportKey.PERCENT: mem_info.percent,
    }
