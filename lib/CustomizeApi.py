# -*- coding: utf-8 -*
import random
from .CustomizeParams import CustomParams

__all__ = 'CustomApi',


class CustomApi:

    @staticmethod
    def api_method_dispatch(api, api_method):
        if api_method == 'business_exception_api':
            return CustomApi.__business_exception_api(api)
        if api_method == 'random_api_path':
            return CustomApi.__random_api_path(api)

    @staticmethod
    def __business_exception_api(api):
        os_arr = ['android', 'ios']
        return (api + '?os=%s') % random.choice(os_arr)

    @staticmethod
    def __random_api_path(api):
        if '{gameId}' in api:
            game_id = CustomParams.random_game_id()
            api = api.replace('{gameId}', game_id.get('gameId'))
        if '{userId}' in api:
            user_id = CustomParams.random_user_id()
            api = api.replace('{userId}', str(user_id.get('userId')))
        if '{decorationId}' in api:
            decoration_id = random.randrange(1, 1370)
            api = api.replace('{decorationId}', str(decoration_id))
        if '{typeId}' in api:
            type_id = random.randrange(1, 29)
            api = api.replace('{typeId}', str(type_id))
        return api
