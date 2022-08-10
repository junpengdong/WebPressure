# -*- coding: utf-8 -*
from .CustomizeParams import CustomParams

__all__ = 'CustomBody',


class CustomBody:

    @staticmethod
    def body_method_dispatch(body_method):
        if body_method == 'random_user_id_list':
            return CustomBody.__random_user_id_list()

    @staticmethod
    def __random_user_id_list():
        return CustomParams.random_user_id_list().get("userIdList")

