# -*- coding: utf-8 -*
import copy
from lib import WebResponseData
from prettytable import PrettyTable

__all__ = 'PerformanceDataPrint', 'DataAnalysisPrint',


class PerformanceDataPrint:

    def __init__(self, key, req_number, exec_time, resp_time_arr, resp_error_arr, sent_arr, receive_arr):
        self.__key = key
        self.__req_number = req_number
        self.__exec_time = "{:.3f}".format(exec_time)
        self.__sec_number = req_number / exec_time
        self.__max_resp_time = "{:.3f}".format(max(resp_time_arr))
        self.__min_resp_time = "{:.3f}".format(min(resp_time_arr))
        self.__avg_resp_time = "{:.3f}".format(sum(resp_time_arr) / len(resp_time_arr))
        self.__max_tps = "{:.3f}".format(self.__sec_number / (float(self.__min_resp_time) / 1000))
        self.__min_tps = "{:.3f}".format(self.__sec_number / (float(self.__max_resp_time) / 1000))
        self.__avg_tps = "{:.3f}".format(self.__sec_number / (float(self.__avg_resp_time) / 1000))
        copy_resp_time_arr = copy.copy(resp_time_arr)
        copy_resp_time_arr.sort()
        self.__resp_time_50 = copy_resp_time_arr[self.get_arr_index(copy_resp_time_arr, 0.5)]
        self.__resp_time_90 = copy_resp_time_arr[self.get_arr_index(copy_resp_time_arr, 0.9)]
        self.__resp_time_95 = copy_resp_time_arr[self.get_arr_index(copy_resp_time_arr, 0.95)]
        self.__resp_time_99 = copy_resp_time_arr[self.get_arr_index(copy_resp_time_arr, 0.99)]
        self.__sent_kb = "{:.2f}".format(sum(sent_arr) / 1000 / exec_time)
        self.__receive_kb = "{:.2f}".format(sum(receive_arr) / 1000 / exec_time)
        slow_query = 0
        for time in resp_time_arr:
            if time > 200:
                slow_query = slow_query + 1
        self.__slow_query = slow_query
        self.__slow_query_rate = "{:.2f}%".format(float(self.__slow_query / req_number) * 100)
        self.__error_query = resp_error_arr.count("0")
        self.__error_query_rate = "{:.2f}%".format(float(self.__error_query / req_number) * 100)

    @staticmethod
    def get_arr_index(arr, percent):
        index = int(len(arr) * percent)
        if index != 0:
            index = index - 1
        return index

    # 同步打印性能分析数据
    def sync_print(self, t):
        if t == 'warm_up':
            print("Warm Up Request End...")
            print("-----------------------------------------------------------------------------")
            print("|                                                                           |")
            print("|                           Warm Up Pressure Data                           |")
            print("|                                                                           |")
            print("-----------------------------------------------------------------------------")
        else:
            WebResponseData.write_data(self.__key, self.__max_resp_time, self.__min_resp_time, self.__avg_resp_time,
                                       self.__max_tps, self.__min_tps, self.__avg_tps, self.__slow_query,
                                       self.__error_query)
            print("Web Api Request End...")
            print("-----------------------------------------------------------------------------")
            print("|                                                                           |")
            print("|                           Web Api Pressure Data                           |")
            print("|                                                                           |")
            print("-----------------------------------------------------------------------------")
        self.append_str("|        Execute Time                |        %s s" % self.__exec_time)
        self.append_str("|        Request Times               |        %s" % self.__req_number)
        self.append_str("|        Request Times/Sec           |        %s" % self.__sec_number)
        self.append_str("|        Max Response Time           |        %s ms" % self.__max_resp_time)
        self.append_str("|        Min Response Time           |        %s ms" % self.__min_resp_time)
        self.append_str("|        Avg Response Time           |        %s ms" % self.__avg_resp_time)
        self.append_str("|        Max TPS                     |        %s" % self.__max_tps)
        self.append_str("|        Min TPS                     |        %s" % self.__min_tps)
        self.append_str("|        Avg TPS                     |        %s" % self.__avg_tps)
        self.append_str("|        50% Line                    |        " + str(self.__resp_time_50) + " ms")
        self.append_str("|        90% Line                    |        " + str(self.__resp_time_90) + " ms")
        self.append_str("|        95% Line                    |        " + str(self.__resp_time_95) + " ms")
        self.append_str("|        99% Line                    |        " + str(self.__resp_time_99) + " ms")
        self.append_str("|        Sent KB/Sec                 |        %s KB" % self.__sent_kb)
        self.append_str("|        Received KB/Sec             |        %s KB" % self.__receive_kb)
        self.append_str("|        Slow Request Times          |        %s" % self.__slow_query)
        self.append_str("|        Slow Request Rate           |        %s" % self.__slow_query_rate)
        self.append_str("|        Error Request Times         |        %s" % self.__error_query)
        self.append_str("|        Error Request Rate          |        %s" % self.__error_query_rate)
        print("-----------------------------------------------------------------------------\n\n")

    @staticmethod
    def append_str(s, c=77):
        length = len(s)
        if length < c:
            for i in range(c - length - 1):
                s = s + " "
        s = s + "|"
        print(s)


class DataAnalysisPrint:

    def __init__(self):
        self.__key_arr = ['max_resp_time', 'min_resp_time', 'avg_resp_time',
                          'max_tps', 'min_tps', 'avg_tps', 'slow_query', 'error_query']

    def data_handle(self, key):
        json_data = WebResponseData.read_data()
        json_obj_arr = json_data.get(key)
        handle_arr = []
        for k in self.__key_arr:
            handle_arr.append(DataAnalysisPrint.data_compare(k, json_obj_arr))
        self.data_print(handle_arr)

    @staticmethod
    def data_compare(key, json_obj_arr):
        value_arr = [d[key] for d in json_obj_arr]
        if len(value_arr) == 0:
            return
        newest_data = value_arr[-1]
        value_arr = value_arr[:len(value_arr) - 1]
        compare_arr = [key]
        for value in value_arr:
            if isinstance(value, int):
                v = int(newest_data) - int(value)
                if v > 0:
                    result = "+%s" % v
                else:
                    result = "%s" % v
            else:
                v = float(newest_data) - float(value)
                if v > 0:
                    result = "+{:.3f}".format(v)
                else:
                    result = "{:.3f}".format(v)
            compare_arr.append("%s(%s)" % (value, result))
        compare_arr.append(newest_data)
        return compare_arr

    @staticmethod
    def data_print(handle_arr):
        tb = PrettyTable()
        tb.field_names = ['key_type', 'index[4]', 'index[3]', 'index[2]', 'index[1]', 'index[0]']
        for data_arr in handle_arr:
            tb.add_row(data_arr)
        print(tb)
