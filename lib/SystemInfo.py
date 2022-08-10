# -*- coding:utf-8 -*
import psutil
import sys

__all__ = 'StressSystemInfo',


class StressSystemInfo:

    @staticmethod
    def __get_cpu_state(interval):
        return psutil.cpu_percent(int(interval))

    @staticmethod
    def __get_memory_state():
        memory = psutil.virtual_memory()
        return int(memory.used / 1024 / 1024), int(memory.total / 1024 / 1024)

    def print_info(self, interval="1"):
        while True:
            cpu_percent = self.__get_cpu_state(interval)
            used_memory, total_memory = self.__get_memory_state()
            end_str = " " * ((100 - int(cpu_percent)) // 3) + "| " + str(used_memory) \
                      + "M/" + str(total_memory) + "M "
            print("\r", end="")
            print("System CPU Info: {}%: ".format(cpu_percent), "▋" * (int(cpu_percent) // 2),
                  end=end_str)
            sys.stdout.flush()
