# -*- coding: utf-8 -*
import sys
import time
import getopt
sys.path.append('../')
from core import *
from lib import *

server = ''
controller = 'all'
function = 'all'
dynamic = None
host = None


class PressureMain:

    def __init__(self):
        self.__request_thread_arr = []
        # 接口响应时间数组
        self.resp_time_arr = []
        # 响应异常数组
        self.resp_error_arr = []
        # 发送数据字节数组
        self.sent_arr = []
        # 接收数据字节数组
        self.receive_arr = []

    @staticmethod
    def do_function(d, req):
        print('pressure api %s\n' % d['api'])
        pressure_main = PressureMain()
        return pressure_main.request_thread(d, req)

    def request_thread(self, data, obj):
        c = obj.get_controller(data)
        f = obj.get_function(data)

        api = obj.get_api(data)
        request_number = obj.get_request_number(data)
        request_type = obj.get_request_type(data)
        headers = obj.get_headers(data)
        complete_time = obj.get_complete_second(data)
        for i in range(request_number):
            params = obj.get_params(data)
            body_data = obj.get_body_data(data)
            self.sent_arr.append(len(str(params).encode('utf-8')) + len(str(headers).encode('utf-8')))
            if request_type == 'get':
                self.__request_thread_arr.append(CustomThreadPool(ApiRequest.get, args=(api, headers, params, body_data)))
            elif request_type == 'post':
                self.__request_thread_arr.append(CustomThreadPool(ApiRequest.post, args=(api, headers, params, body_data)))
            elif request_type == 'put':
                self.__request_thread_arr.append(CustomThreadPool(ApiRequest.put, args=(api, headers, params, body_data)))
            else:
                print('error request_type')
                sys.exit(1)
        start_time = time.time()
        if complete_time > 0:
            self.__slow_start_thread(complete_time)
        else:
            self.__fast_start_thread()
        exec_time = time.time() - start_time
        # print('all thread request finish.\n')
        self.__join_thread()
        # 数据打印
        data_row = self.__performance_data_print(f, request_number, exec_time)
        # 数据写入csv中
        csv_file = CsvFile(server, c, f, data_row)
        csv_file.csv_handle()
        return {
            'controller': c,
            'function': f,
            'data': self.resp_time_arr
        }

    def __fast_start_thread(self):
        try:
            for thread in self.__request_thread_arr:
                thread.start()
        except Exception as e:
            return e

    def __slow_start_thread(self, ct):
        try:
            slow_time = round(((ct * 1000) / len(self.__request_thread_arr)) / 1000, 3)
            for thread in self.__request_thread_arr:
                thread.start()
                time.sleep(slow_time)
        except Exception as e:
            return e

    def __join_thread(self):
        for thread in self.__request_thread_arr:
            if thread.is_alive():
                thread.join()
                result = thread.get_result()
            else:
                result = thread.get_result()

            if result is None:
                self.resp_error_arr.append("0")
            else:
                self.receive_arr.append(len(str(result.text).encode('utf-8')))
                if result.status_code != 200:
                    self.resp_error_arr.append("0")
                else:
                    self.resp_time_arr.append(result.elapsed.microseconds / 1000)

    def __performance_data_print(self, f, n, et):
        data_print = PerformanceDataPrint(f, n, et, self.resp_time_arr, self.resp_error_arr,
                                          self.sent_arr, self.receive_arr)
        data_print.analysis_print()
        return data_print.get_data_row()

    def __performance_data_plot(self, c, f, plot_obj):
        plot_obj.data_plot(c, f, self.resp_time_arr)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "(hH)s:c:f:d:", ['help=', 'server=', 'controller=', 'function=', 'dynamic='])
    if len(opts) == 0:
        print('Usage python PressureStart.py -s server-name -c controller-name -f function-name -d')
        sys.exit(1)

    if sys.argv[1] in ('-h', '-H', '--help'):
        print('Usage python PressureStart.py -s server-name -c controller-name -f function-name -d')
        sys.exit(1)

    if sys.argv[1] in ('-s', '--server', '-c', '--controller', '-f', '--function', '-d', '--dynamic'):
        for opt, arg in opts:
            if opt in ('-s', '--server'):
                server = arg
            if opt in ('-c', '--controller'):
                controller = arg
            if opt in ('-f', '--function'):
                function = arg
            if opt in ('-d', '--dynamic'):
                dynamic = arg

    if server == '':
        print('Usage python PressureStart.py -s server-name -c controller-name -f function-name -d')
        sys.exit(1)

    if dynamic is not None:
        server_host = ServerHost()
        host = server_host.get_host(server)
    api_request_data = ApiRequestData(server, controller, function, host)
    json_data_arr = api_request_data.get_json_data()

    thread_arr = []
    for json_data in json_data_arr:
        thread_arr.append(CustomThreadPool(PressureMain.do_function, args=(json_data, api_request_data)))

    # 打印系统详情
    interval = "1"
    system_info = StressSystemInfo()
    system_info_thread = CustomThreadPool(system_info.print_info, interval)
    system_info_thread.setDaemon(True)
    system_info_thread.start()

    for t in thread_arr:
        t.start()

    r_arr = []
    for t in thread_arr:
        if t.is_alive():
            t.join()
            r = t.get_result()
        else:
            r = t.get_result()
        if r is not None:
            r_arr.append(r)

    # 数据绘图
    data_plot = PerformanceDataPlot(server)
    for r in r_arr:
        data_plot.data_plot(r.get('controller'), r.get('function'), r.get('data'))
