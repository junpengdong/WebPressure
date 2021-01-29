import requests
import traceback

__all__ = 'ApiRequest',


class ApiRequest:

    @staticmethod
    def get(url, headers, params):
        try:
            response = requests.get(url=url, headers=headers, params=params)
            return response.elapsed.microseconds
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 0

    @staticmethod
    def post(url, headers, params):
        try:
            response = requests.post(url=url, headers=headers, data=params)
            return response.elapsed.microseconds
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 0
