from lib import *
from core import *
import time

thread_arr = []
# 读取request_data.json的key配置
key = 'es_library'
# 接口响应时间数组
resp_time_arr = []
# 绘图横坐标数组
x_arr = []
# 响应异常数组
resp_error_arr = []
# 发送数据字节数组
sent_arr = []
# 接收数据字节数组
receive_arr = []


def fast_req():
    for thread in thread_arr:
        thread.setDaemon(True)
        thread.start()


def slow_req(t):
    slow_time = round(((t * 1000) / len(thread_arr)) / 1000, 3)
    for thread in thread_arr:
        thread.setDaemon(True)
        thread.start()
        time.sleep(slow_time)


def thread_join():
    for thread in thread_arr:
        thread.join()
        result = thread.get_result()

        if result is None:
            resp_error_arr.append("0")
        else:
            receive_arr.append(len(str(result.text).encode('utf-8')))
            if result.status_code != 200:
                resp_error_arr.append("0")
            else:
                resp_time_arr.append(result.elapsed.microseconds / 1000)


if __name__ == '__main__':
    web_req_data = WebRequestData()
    req_number = web_req_data.get_req_number(key)
    for i in range(1, req_number + 1):
        url = web_req_data.get_url(key)
        headers = web_req_data.get_headers(key)
        params = web_req_data.get_params(key)
        sent_arr.append(len(str(params).encode('utf-8')) + len(str(headers).encode('utf-8')))
        thread_arr.append(CustomThreadPool(ApiRequest.get, args=(url, headers, params)))

    req_time = web_req_data.get_req_time(key)
    start_time = time.time()
    if req_time > 0:
        print('slow_req')
        slow_req(req_time)
    else:
        print('fast_req')
        fast_req()
    thread_join()
    exec_time = time.time() - start_time

    data_print = PerformanceDataPrint(req_number, exec_time, resp_time_arr, resp_error_arr, sent_arr, receive_arr)
    data_print.sync_print()
