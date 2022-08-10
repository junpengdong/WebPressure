# -*- coding: utf-8 -*
import random
from .CustomizeParams import CustomParams

__all__ = 'CustomHeaders',


class CustomHeaders:

    @staticmethod
    def headers_method_dispatch(headers_method):
        if headers_method == 'business_exception_headers':
            return CustomHeaders.__business_exception_headers()
        elif headers_method == 'random_user_id':
            return CustomHeaders.__random_user_id()
        elif headers_method == 'random_user_id_and_language':
            return CustomHeaders.__random_user_id_and_language()

    @staticmethod
    def __business_exception_headers():
        app_version_arr = [900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]
        user_id = random.randrange(10, 1000) * 16
        return {
            "userId": str(user_id),
            "appVersion": str(random.choice(app_version_arr))
        }

    @staticmethod
    def __random_user_id():
        user_id = CustomParams.random_user_id().get('userId')
        return {"userId": str(user_id)}

    @staticmethod
    def __random_user_id_and_language():
        user_id = CustomParams.random_user_id().get('userId')
        return {"userId": str(user_id), "language": "en_US"}