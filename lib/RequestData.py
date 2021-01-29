import json

__all__ = 'WebRequestData',


class WebRequestData:

    url = ''
    params = {}
    headers = {}

    def __init__(self):
        with open('../data/request_data.json', 'r', encoding='utf=8') as json_data:
            json_obj = json.load(json_data)
            self.url = json_obj['url']
            self.params = json_obj['params']
            self.headers = json_obj['headers']

    def get_url(self):
        # 可以自定义url
        return self.url

    def get_params(self):
        # 可以自定义params
        return self.params

    def get_headers(self):
        # 可以自定headers
        return self.headers
