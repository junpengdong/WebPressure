# -*- coding: utf-8 -*
import requests
import traceback

__all__ = 'ApiRequest',


class ApiRequest:

    @staticmethod
    def get(url='', headers=None, params=None, data=None):
        try:
            return requests.get(url=url, headers=headers, params=params, json=data)
        except Exception as e:
            # print(e)
            traceback.print_exc()
            return None

    @staticmethod
    def post(url='', headers=None, params=None, data=None):
        try:
            return requests.post(url=url, headers=headers, params=params, json=data)
        except Exception as e:
            # print(e)
            traceback.print_exc()
            return None

    @staticmethod
    def put(url='', headers=None, params=None, data=None):
        try:
            return requests.put(url=url, headers=headers, params=params, json=data)
        except Exception as e:
            # print(e)
            traceback.print_exc()
            return None
