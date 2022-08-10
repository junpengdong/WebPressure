# -*- coding: utf-8 -*
import os
import json
import random
from .CustomizeApi import CustomApi
from .CustomizeParams import CustomParams
from .CustomizeHeaders import CustomHeaders
from .CustomizeBody import CustomBody

__all__ = 'ApiRequestData',


class ApiRequestData:

    def __init__(self, s, c, f, h):
        self.__server = s
        self.__controller = c
        self.__function = f
        self.__filter_params()
        self.__host_json = 'Server.json'
        self.__api_key = 'api'
        self.__api_method_key = 'api_method'
        self.__request_type_key = 'request_type'
        self.__host_key = 'host'
        self.__params_method_key = 'params_method'
        self.__params_key = 'params'
        self.__body_method_key = 'body_method'
        self.__body_key = 'body'
        self.__headers_method_key = 'headers_method'
        self.__headers_key = 'headers'
        self.__request_number_key = 'request_number'
        self.__complete_second_key = 'complete_second'
        self.__controller_key = 'controller'
        self.__function_key = 'function'
        self.__base_dir = '../data/request/'
        self.__base_json_dir = '../data/request/%s/'
        self.__base_json_file = '../data/request/%s/%s'
        self.__json_data_arr = self.__init_data(h)

    def get_api(self, json_data):
        api = json_data.get(self.__api_key)
        api_method = json_data.get(self.__api_method_key)
        if api_method is not None and api_method != '':
            return CustomApi.api_method_dispatch(api, api_method)
        else:
            return api

    def get_request_type(self, json_data):
        request_type = json_data.get(self.__request_type_key)
        return request_type

    def get_params(self, json_data):
        params_method = json_data.get(self.__params_method_key)
        if params_method is not None and params_method != '':
            params = CustomParams.params_method_dispatch(params_method)
        else:
            params = json_data.get(self.__params_key)
            if params is not None and params != '':
                params = json.loads(params)
        return params

    def get_body_data(self, json_data):
        body_method = json_data.get(self.__body_method_key)
        if body_method is not None and body_method != '':
            body = CustomBody.body_method_dispatch(body_method)
        else:
            body = json_data.get(self.__body_key)
            if body is not None and body != '':
                body = json.loads(body)
        return body

    def get_headers(self, json_data):
        headers_method = json_data.get(self.__headers_method_key)
        if headers_method is not None and headers_method != '':
            headers = CustomHeaders.headers_method_dispatch(headers_method)
        else:
            headers = json_data.get(self.__headers_key)
            if headers is not None and headers != '':
                headers = json.loads(headers)
        return headers

    def get_request_number(self, json_data):
        request_number = json_data.get(self.__request_number_key)
        return request_number

    def get_complete_second(self, json_data):
        complete_second = json_data.get(self.__complete_second_key)
        return complete_second

    def get_controller(self, json_data):
        return json_data.get(self.__controller_key)

    def get_function(self, json_data):
        return json_data.get(self.__function_key)

    def __filter_params(self):
        if self.__controller == 'all':
            self.__function = 'all'

    def get_json_data(self):
        return self.__json_data_arr

    def __init_data(self, host):
        file_name_arr = self.__file_names()
        data = self.__filter_controller(file_name_arr)
        step1_data = self.__data_handle_step1(data, host)
        step2_data = self.__data_handle_step2(step1_data)
        return step2_data

    def __data_handle_step1(self, data, host=None):
        step1_data = {}
        file_data_arr = []
        for file in data:
            if host is None:
                host_json_path = self.__base_json_file % (self.__server, self.__host_json)
                host_json_obj = self.__read_data(host_json_path)
                host = host_json_obj.get(self.__host_key)
            file_name_path = self.__base_json_file % (self.__server, file)
            file_data_obj = self.__read_data(file_name_path)
            if self.__function == 'all':
                for k2, v2 in file_data_obj.items():
                    v2[self.__controller_key] = file.split('.')[0]
                    v2[self.__function_key] = k2
                    file_data_arr.append(v2)
            else:
                if self.__function.__contains__(','):
                    for f in self.__function.split(','):
                        file_data = file_data_obj.get(f)
                        if file_data is not None:
                            file_data[self.__controller_key] = f.split('.')[0]
                            file_data[self.__function_key] = f
                            file_data_arr.append(file_data)
                else:
                    file_data = file_data_obj.get(self.__function)
                    if file_data is not None:
                        file_data[self.__controller_key] = file.split('.')[0]
                        file_data[self.__function_key] = self.__function
                        file_data_arr.append(file_data)
        step1_data[host] = file_data_arr
        return step1_data

    def __data_handle_step2(self, step1_data):
        api_data_arr = []
        for k, v in step1_data.items():
            for obj in v:
                obj[self.__api_key] = k + obj[self.__api_key]
                api_data_arr.append(obj)
        return api_data_arr

    def __filter_controller(self, data):
        if self.__controller == 'all':
            return data
        else:
            for file_name in data:
                if not file_name.__contains__(self.__controller):
                    data.remove(file_name)
            return data

    def __file_names(self):
        file_name_arr = []
        dir_path = os.path.abspath(self.__base_json_dir % self.__server)
        for file_name in os.listdir(dir_path):
            if file_name == self.__host_json:
                continue
            file_name_arr.append(file_name)
        return file_name_arr

    @staticmethod
    def __read_data(file_path):
        # with open(file_path, 'r', encoding='utf=8') as content:
        with open(file_path, 'r') as content:
            return json.load(content)

    @staticmethod
    def __dir_names(base_dir):
        dir_name_arr = []
        for file in os.listdir(base_dir):
            if not os.path.isfile(os.path.join(base_dir, file)):
                dir_name_arr.append(file)
        return dir_name_arr
