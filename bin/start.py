from lib import *

if __name__ == '__main__':
    request_data = WebRequestData()
    ApiRequest.get()
    print(request_data.url)
    print("执行脚本")