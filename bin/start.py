from lib import *
from core import *
import time


class ScriptMain:

    def __init__(self):
        self.thread_arr = []
        # 读取request_data.json的key配置
        self.key = 'es_library'
        # 接口响应时间数组
        self.resp_time_arr = []
        # 响应异常数组
        self.resp_error_arr = []
        # 发送数据字节数组
        self.sent_arr = []
        # 接收数据字节数组
        self.receive_arr = []

    def init_params(self):
        self.thread_arr = []
        self.resp_time_arr = []
        self.resp_error_arr = []
        self.sent_arr = []
        self.receive_arr = []

    def fast_req(self):
        for thread in self.thread_arr:
            thread.setDaemon(True)
            thread.start()

    def slow_req(self, t):
        slow_time = round(((t * 1000) / len(self.thread_arr)) / 1000, 3)
        for thread in self.thread_arr:
            thread.setDaemon(True)
            thread.start()
            time.sleep(slow_time)

    def thread_join(self):
        for thread in self.thread_arr:
            thread.join()
            result = thread.get_result()

            if result is None:
                self.resp_error_arr.append("0")
            else:
                self.receive_arr.append(len(str(result.text).encode('utf-8')))
                if result.status_code != 200:
                    self.resp_error_arr.append("0")
                else:
                    self.resp_time_arr.append(result.elapsed.microseconds / 1000)

    # 接口压测
    def pressure_req_api(self, n, data_obj, t=None):
        for i in range(1, n + 1):
            url = data_obj.get_url(self.key)
            headers = data_obj.get_headers(self.key)
            params = data_obj.get_params(self.key)
            self.sent_arr.append(len(str(params).encode('utf-8')) + len(str(headers).encode('utf-8')))
            self.thread_arr.append(CustomThreadPool(ApiRequest.get, args=(url, headers, params)))

        req_time = data_obj.get_req_time(self.key)
        start_time = time.time()
        if req_time > 0:
            self.slow_req(req_time)
        else:
            self.fast_req()
        self.thread_join()
        exec_time = time.time() - start_time

        data_print = PerformanceDataPrint(n, exec_time, self.resp_time_arr, self.resp_error_arr,
                                          self.sent_arr, self.receive_arr)
        data_print.sync_print(t)


if __name__ == '__main__':
    web_req_data = WebRequestData()
    script_main = ScriptMain()
    key = script_main.key
    warm_up = web_req_data.get_warm_up(key)
    if warm_up > 0:
        print("预热请求开始...")
        script_main.pressure_req_api(warm_up, web_req_data, t='warm_up')
    script_main.init_params()
    req_number = web_req_data.get_req_number(key)
    print("接口请求开始...")
    script_main.pressure_req_api(req_number, web_req_data)

    # 性能数据处理
    data_handle = PerformanceDataHandle()
    x, y = data_handle.show_type_dispatch(script_main.resp_time_arr,
                                          web_req_data.get_resp_data_handle(key))

    # 性能数据绘图
    data_plot = PerformanceDataPlot()
    data_plot.data_plot_dispatch(x, y, web_req_data.get_resp_show(key))
