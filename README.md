# WebPressure
Web接口压测python项目

### 2021-02-02 14:55
项目还在完善当中

### 2021-02-02 16:23
##### 压测功能已完善

### request_data.json配置说明
```
{
    "es_library": {
        "url": "http://172.17.21.21:8777/api/v1/find/data",
        "c_params_method": "random_append_word",
        "params": "",
        "headers": "",
        "warm_up": 100,
        "req_number": 100,
        "req_type": "get",
        "req_time": 0,
        "resp_data_handle": "medium",
        "resp_show": "line"
    }
}
```
处理json类: RequestData.py
* es_library: 测试方法描述，例子中是对es的词库压测，会根据这个key获取对应api的参数
* url: api地址
* c_params_method: 自定义生成body参数方法（可以看源码怎么使用）
* params: 如果不需要自定义生成body参数，则可以使用固定参数，{"key": "value"}
* headers: 请求头部参数，暂时没添加自定义头部参数，如需要可自行添加对应逻辑
* warm_up: 预热请求数量，执行压测前可以先进行预热请求
* req_number: 请求次数
* req_type: 请求类型（目前只支持get跟post）
* req_time: 指定多少秒内完成req_number请求，例如req_number: 100, req_time 10，则是10秒内完成100次请求，即每秒并发10个，不过也需要看压测机器的性能，比如req_number: 1000，req_time: 1则不一定能够在1秒内完成1000次请求
* resp_data_handle: 响应数据处理类型（low: 只展示最小，平均，最大响应时间、medium: 数据长度小于50则跟high相同，否则按数据长度的百分之10展示、high: 不处理，全部展示）
resp_show: 响应数据绘图类型（目前只支持bar跟line）
