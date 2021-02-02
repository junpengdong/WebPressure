# WebPressure
Web接口压测python项目，通过项目学习Python

### 2021-01-29
项目还在完善当中

### 2021-02-02
#### 压测功能已完善
* 压测脚本功能也调通
* 性能数据分析计算公式可能存在不足之处，或理解不充分，造成数据计算存在误差，欢迎指点纠正
* 打印信息如下:
```
-----------------------------------------------------------------------------
|                                                                           |
|                             压测请求性能数据                                 |
|                                                                           |
-----------------------------------------------------------------------------
|        Execute Time                |        0.855 s                       |
|        Request Times               |        100                           |
|        Request Times/Sec           |        116.91586375299481            |
|        Max Response Time           |        755.041 ms                    |
|        Min Response Time           |        284.764 ms                    |
|        Avg Response Time           |        516.633 ms                    |
|        Max TPS                     |        410.571                       |
|        Min TPS                     |        154.847                       |
|        Avg TPS                     |        226.304                       |
|        50% Line                    |        508.923 ms                    |
|        90% Line                    |        722.084 ms                    |
|        95% Line                    |        733.499 ms                    |
|        99% Line                    |        742.978 ms                    |
|        Sent KB/Sec                 |        2.01 KB                       |
|        Received KB/Sec             |        3.86 KB                       |
|        Slow Request Times          |        100                           |
|        Slow Request Rate           |        100.00%                       |
|        Error Request Times         |        0                             |
|        Error Request Rate          |        0.00%                         |
-----------------------------------------------------------------------------
```

### Python压测脚本性能数据绘图库
* pip install matplotlib

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
