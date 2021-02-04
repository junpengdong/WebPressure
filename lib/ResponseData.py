import json

__all__ = 'WebResponseData',


class WebResponseData:

    @staticmethod
    def write_data(key, max_resp_time, min_resp_time, avg_resp_time,
                   max_tps, min_tps, avg_tps, slow_query, error_query):
        json_data = WebResponseData.read_data()
        data_arr = json_data.get(key)
        if data_arr is None:
            data_arr = []
        json_obj = {
            "max_resp_time": max_resp_time,
            "min_resp_time": min_resp_time,
            "avg_resp_time": avg_resp_time,
            "max_tps": max_tps,
            "min_tps": min_tps,
            "avg_tps": avg_tps,
            "slow_query": slow_query,
            "error_query": error_query
        }
        data_arr.append(json_obj)
        if len(data_arr) > 5:
            data_arr = data_arr[-5:]
        json_data[key] = data_arr
        with open('../data/response_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4)

    @staticmethod
    def read_data():
        with open('../data/response_data.json', 'r', encoding='utf=8') as json_str:
            return json.load(json_str)
