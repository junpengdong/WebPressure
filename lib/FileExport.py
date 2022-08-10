# -*- coding: utf-8 -*
import os
import csv

__all__ = 'CsvFile',


class CsvFile:

    def __init__(self, s, c, f, r):
        self.__base_server_dir = '../data/response/%s/' % s
        self.__base_controller_dir = '../data/response/%s/%s/' % (s, c)
        self.__csv_path = self.__base_controller_dir + ('%s_performance_data.csv' % f)
        self.__row = r
        self.__init_os()

    def __init_os(self):
        if not os.path.exists(self.__base_server_dir):
            os.makedirs(self.__base_server_dir)
        if not os.path.exists(self.__base_controller_dir):
            os.makedirs(self.__base_controller_dir)

    def csv_handle(self):
        if self.__file_exist():
            self.__append_csv()
        else:
            self.__write_csv()

    def __file_exist(self):
        return os.path.exists(self.__csv_path)

    def __write_csv(self):
        with open(self.__csv_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['执行时间(秒)', '请求次数', '每秒请求数', '最大响应时间(毫秒)', '最小响应时间(毫秒)',
                             '平均响应时间(毫秒)', '最大TPS', '最小TPS', '平均TPS', '50%请求响应时间(毫秒)',
                             '90%请求响应时间(毫秒)', '95%请求响应时间(毫秒)', '99%请求响应时间(毫秒)', '每秒发送数据量(KB)',
                             '每秒接收数据量(KB)', '慢请求数', '慢请求率(%)', '错误请求数', '错误请求率(%)'])
            handle_row = []
            for i in range(len(self.__row)):
                if i == 1:
                    handle_row.append(self.__row[i])
                    continue
                handle_row.append('%s(0)' % self.__row[i])
            writer.writerow(handle_row)

    def __append_csv(self):
        pre_row = []
        with open(self.__csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
            if len(rows) > 1:
                pre_row = rows[-1]
        if len(pre_row) == 0:
            return
        compare_row = []
        for i in range(len(self.__row)):
            temp = '%s(%s)'
            data = str(self.__row[i]).split('(')[0]
            if i == 1:
                compare_row.append(data)
                continue
            pre_data = str(pre_row[i]).split('(')[0]
            r = float(data) - float(pre_data)
            if r > 0:
                r = '+%s' % '{:.3f}'.format(r)
            else:
                r = '{:.3f}'.format(r)
            compare_row.append(temp % (data, r))
        with open(self.__csv_path, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(compare_row)
