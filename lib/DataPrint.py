# -*- coding: utf-8 -*
import copy

__all__ = 'PerformanceDataPrint',


class PerformanceDataPrint:

    def __init__(self, function, req_number, exec_time, resp_time_arr, resp_error_arr, sent_arr, receive_arr):
        self.__function = function
        self.__req_number = req_number
        self.__exec_time = "{:.6f}".format(exec_time)
        self.__sec_number = req_number / exec_time
        self.__max_resp_time = "{:.3f}".format(max(resp_time_arr))
        self.__min_resp_time = "{:.3f}".format(min(resp_time_arr))
        self.__avg_resp_time = "{:.3f}".format(sum(resp_time_arr) / len(resp_time_arr))
        self.__max_tps = "{:.3f}".format(self.__sec_number / (float(self.__min_resp_time) / 1000))
        self.__min_tps = "{:.3f}".format(self.__sec_number / (float(self.__max_resp_time) / 1000))
        self.__avg_tps = "{:.3f}".format(self.__sec_number / (float(self.__avg_resp_time) / 1000))
        copy_resp_time_arr = copy.copy(resp_time_arr)
        copy_resp_time_arr.sort()
        self.__resp_time_50 = copy_resp_time_arr[self.__get_arr_index(copy_resp_time_arr, 0.5)]
        self.__resp_time_90 = copy_resp_time_arr[self.__get_arr_index(copy_resp_time_arr, 0.9)]
        self.__resp_time_95 = copy_resp_time_arr[self.__get_arr_index(copy_resp_time_arr, 0.95)]
        self.__resp_time_99 = copy_resp_time_arr[self.__get_arr_index(copy_resp_time_arr, 0.99)]
        self.__sent_kb = "{:.2f}".format(sum(sent_arr) / 1000 / exec_time)
        self.__receive_kb = "{:.2f}".format(sum(receive_arr) / 1000 / exec_time)
        slow_query = 0
        for time in resp_time_arr:
            if time > 200:
                slow_query = slow_query + 1
        self.__slow_query = slow_query
        self.__slow_query_rate = "{:.2f}".format(float(self.__slow_query / req_number) * 100)
        self.__error_query = resp_error_arr.count("0")
        self.__error_query_rate = "{:.2f}".format(float(self.__error_query / req_number) * 100)

    @staticmethod
    def __get_arr_index(arr, percent):
        index = int(len(arr) * percent)
        if index != 0:
            index = index - 1
        return index

    def get_data_row(self):
        return [self.__exec_time, self.__req_number, "{:.3f}".format(self.__sec_number), self.__max_resp_time,
                self.__min_resp_time, self.__avg_resp_time, self.__max_tps, self.__min_tps,
                self.__avg_tps, self.__resp_time_50, self.__resp_time_90, self.__resp_time_95,
                self.__resp_time_99, self.__sent_kb, self.__receive_kb, self.__slow_query,
                self.__slow_query_rate, self.__error_query, self.__error_query_rate]

    # 同步打印性能分析数据
    def analysis_print(self):
        s = '-----------------------------------------------------------------------------\n'
        s = s + '|                                                                           |\n' \
            + self.__append_title_str('%s Pressure Data' % self.__function) \
            + '|                                                                           |\n' \
            + '-----------------------------------------------------------------------------\n' \
            + self.__append_str("|        Execute Time                |              %s s" % self.__exec_time) \
            + self.__append_str("|        Request Times               |              %s" % self.__req_number) \
            + self.__append_str("|        Request Times/Sec           |              %s" % "{:.3f}"
                                .format(self.__sec_number)) \
            + self.__append_str("|        Max Response Time           |              %s ms" % self.__max_resp_time) \
            + self.__append_str("|        Min Response Time           |              %s ms" % self.__min_resp_time) \
            + self.__append_str("|        Avg Response Time           |              %s ms" % self.__avg_resp_time) \
            + self.__append_str("|        Max TPS                     |              %s" % self.__max_tps) \
            + self.__append_str("|        Min TPS                     |              %s" % self.__min_tps) \
            + self.__append_str("|        Avg TPS                     |              %s" % self.__avg_tps) \
            + self.__append_str("|        50% Line                    |              "
                                + str(self.__resp_time_50) + " ms") \
            + self.__append_str("|        90% Line                    |              "
                                + str(self.__resp_time_90) + " ms") \
            + self.__append_str("|        95% Line                    |              "
                                + str(self.__resp_time_95) + " ms") \
            + self.__append_str("|        99% Line                    |              "
                                + str(self.__resp_time_99) + " ms") \
            + self.__append_str("|        Sent KB/Sec                 |              %s KB" % self.__sent_kb) \
            + self.__append_str("|        Received KB/Sec             |              %s KB" % self.__receive_kb) \
            + self.__append_str("|        Slow Request Times          |              %s" % self.__slow_query) \
            + self.__append_str("|        Slow Request Rate           |              " + self.__slow_query_rate + "%") \
            + self.__append_str("|        Error Request Times         |              %s" % self.__error_query) \
            + self.__append_str("|        Error Request Rate          |              "
                                + self.__error_query_rate + "%") \
            + '-----------------------------------------------------------------------------\n\n'
        print('\n')
        print(s)

    @staticmethod
    def __append_title_str(s, c=77):
        length = len(s)
        r_length = c - length
        for i in range(int(r_length / 2)):
            s = " " + s
        s = "|" + s
        length = len(s)
        r_length = c - length
        for i in range(int(r_length) - 1):
            s = s + " "
        s = s + "|\n"
        return s

    @staticmethod
    def __append_str(s, c=77):
        length = len(s)
        if length < c:
            for i in range(c - length - 1):
                s = s + " "
        s = s + "|\n"
        return s
