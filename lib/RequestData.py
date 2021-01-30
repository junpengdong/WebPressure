# -*- coding: utf-8 -*
import json
import random

__all__ = 'WebRequestData',


class WebRequestData:

    def __init__(self):
        with open('../data/request_data.json', 'r', encoding='utf=8') as json_str:
            self.__json_data = json.load(json_str)

    # 获取请求地址
    def get_url(self, key):
        url = self.__json_data[key]['url']
        return url

    # 获取请求参数
    def get_params(self, key):
        c_params_method = self.__json_data[key]['c_params_method']
        if c_params_method != '' and c_params_method is not None:
            return self.custom_params(c_params_method)
        else:
            return self.__json_data[key]['params']

    # 获取请求头部参数
    def get_headers(self, key):
        headers = self.__json_data[key]['headers']
        return headers

    # 获取预热请求次数
    def get_warm_up(self, key):
        warm_up = self.__json_data[key]['warm_up']
        return warm_up

    # 获取请求次数
    def get_req_number(self, key):
        req_number = self.__json_data[key]['req_number']
        return req_number

    # 获取请求类型
    def get_req_type(self, key):
        req_type = self.__json_data[key]['req_type']
        return req_type

    # 获取完成所有请求时间
    def get_req_time(self, key):
        req_time = self.__json_data[key]['req_time']
        return req_time

    # 获取绘图类型
    def get_resp_show(self, key):
        resp_show = self.__json_data[key]['resp_show']
        return resp_show

    # 自定义请求参数
    def custom_params(self, method):
        if method == 'random_append_word':
            return self.random_append_word()

    @staticmethod
    def random_append_word():
        letter_arr = ['a', 'b', 'c', 'd', 'e', 'f']
        count = 0
        word = ''
        while count < random.randrange(1, 5):
            count = count + 1
            word = word + random.choice(letter_arr)

        return {
            'keyword': word
        }
