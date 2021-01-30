# -*- coding: utf-8 -*
import copy

__all__ = 'PerformanceDataPrint',


class PerformanceDataPrint:

    def __init__(self, req_number, exec_time, resp_time_arr, resp_error_arr, sent_arr, receive_arr):
        self.__req_number = req_number
        self.__exec_time = exec_time
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
        self.__receive_kb = "{:.2f}".format(sum(receive_arr) / 1000/ exec_time)
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
    def sync_print(self):
        print("执行请求时间: %s s" % self.__exec_time)
        print("请求次数: %s" % self.__req_number)
        print("每秒请求数: %s" % self.__sec_number)
        print()
        print("最大响应时间: %s ms" % self.__max_resp_time)
        print("最小响应时间: %s ms" % self.__min_resp_time)
        print("平均响应时间: %s ms" % self.__avg_resp_time)
        print()
        print("最大TPS: %s" % self.__max_tps)
        print("最小TPS: %s" % self.__min_tps)
        print("平均TPS: %s" % self.__avg_tps)
        print()
        print("百分之50请求响应时间: %s ms" % self.__resp_time_50)
        print("百分之90请求响应时间: %s ms" % self.__resp_time_90)
        print("百分之95请求响应时间: %s ms" % self.__resp_time_95)
        print("百分之99请求响应时间: %s ms" % self.__resp_time_99)
        print()
        print("每秒发送数据量: %s KB" % self.__sent_kb)
        print("每秒接收数据量: %s KB" % self.__receive_kb)
        print()
        print("慢请求次数: %s" % self.__slow_query)
        print("慢请求率: %s" % self.__slow_query_rate)
        print()
        print("错误请求次数: %s" % self.__error_query)
        print("错误请求率: %s" % self.__error_query_rate)
