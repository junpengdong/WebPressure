# -*- coding: utf-8 -*
import csv
import random
import os
import csv

__all__ = 'CustomParams',

daily_user_arr = []

game_id_list = []

sub_key_list = ['1', 'BlockShopDat', 'CommandListDat', 'CommonActivityDat', 'CubeStoreFreeTicke', 'CustomShopDat',
                'DayKeyRecor', 'FreeGiftDat', 'GamePropDat', 'GameRecor', 'GameSurve', 'HeadFrameDat', 'LoginRewardDat',
                'PluginActivityDat', 'SumRecharg', 'TreasureChallengeDat', 'TriggerGiftDat', 'UpdateDat',
                'newPlayerData']

rank_key_list = ["g1030.WIN", "g1041.TotalFight", "g1041.TotalCollect", "g1019.level", "g1014.police", "g1023.score",
                 "g1023.winner", "g1048.forever.rank"]


def init_daily_user_csv():
    global daily_user_arr
    if len(daily_user_arr) == 0:
        with open('../../daily-user.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for item in reader:
                daily_user_arr.append(int(item[0]))
    return daily_user_arr


def init_game_id_csv():
    global game_id_list
    if len(game_id_list) == 0:
        with open('../resource/game-id.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for item in reader:
                game_id_list.append(item[0])
    return game_id_list


class CustomParams:

    def __init__(self, s, c, f, r):
        self.__base_controller_dir = '../data/'
        self.__csv_path = self.__base_controller_dir + ('daily-user.csv')
        self.__row = r

    @staticmethod
    def params_method_dispatch(params_method):
        if params_method == 'random_keyword':
            return CustomParams.__random_keyword()
        elif params_method == 'business_exception_params':
            return CustomParams.__business_exception()
        elif params_method == 'random_user_id':
            return CustomParams.random_user_id()
        elif params_method == 'random_game_id':
            return CustomParams.random_game_id()
        elif params_method == 'random_user_id_and_game_id':
            return CustomParams.__random_user_id_and_game_id()
        elif params_method == 'random_user_id_and_game_ids':
            return CustomParams.__random_user_id_and_game_ids()
        elif params_method == 'random_user_id_and_user_ids':
            return CustomParams.__random_user_id_and_user_ids()
        elif params_method == 'random_user_id_list':
            return CustomParams.random_user_id_list()
        elif params_method == 'random_user_ids':
            return CustomParams.random_user_ids()
        elif params_method == 'random_user_id_and_sub_key_and_table_name':
            return CustomParams.random_user_id_and_sub_key_and_table_name()
        elif params_method == 'random_member_id_and_rank_key':
            return CustomParams.random_member_id_and_rank_key()
        elif params_method == 'random_rank_key_and_offset':
            return CustomParams.random_rank_key_and_offset()

    @staticmethod
    def random_user_id_and_sub_key_and_table_name():
        user_id = CustomParams.random_user_id().get("userId")
        sub_key = CustomParams.random_sub_key().get("subKey")
        return {
            'userId': user_id,
            'subKey': sub_key,
            'tableName': 'prod_g1008'
        }

    @staticmethod
    def userid_from_active():

        return

    @staticmethod
    def __random_keyword():
        letter_arr = ['a', 'b', 'c', 'd', 'e', 'f']
        count = 0
        word = ''
        while count < random.randrange(1, 5):
            count = count + 1
            word = word + random.choice(letter_arr)
        return {
            'keyword': word
        }

    @staticmethod
    def __business_exception():
        request_params_arr = []
        random_num = random.randrange(1, 11)
        for n in range(random_num):
            url_arr = []
            for i in range(1, 1000):
                url_arr.append('/api/v1/url-%s' % i)
            request_params = '{"key1": "value1", "key2": "value2", "key3": "value3", "key4": "value4"}'
            response_code = random.randrange(2, 10000)
            response_msg = "pressure business exception api, code = %s" % response_code
            request_params_arr.append({
                "url": random.choice(url_arr),
                "requestParams": request_params,
                "responseCode": str(response_code),
                "responseMsg": response_msg
            })
        return request_params_arr

    @staticmethod
    def random_user_id():
        user_id_list = init_daily_user_csv()
        total_count = len(user_id_list)
        index = random.randrange(0, total_count)
        user_id = user_id_list[index]
        return {"userId": user_id}

    @staticmethod
    def random_user_id_and_language():
        user_id_list = init_daily_user_csv()
        total_count = len(user_id_list)
        index = random.randrange(0, total_count)
        user_id = user_id_list[index]
        return {"userId": user_id, "language": "en_US"}

    @staticmethod
    def random_game_id():
        game_ids = init_game_id_csv()
        total_count = len(game_ids)
        index = random.randrange(0, total_count)
        game_id = game_ids[index]
        return {"gameId": game_id}

    @staticmethod
    def __random_user_id_and_game_id():
        user_id = CustomParams.random_user_id().get('userId')
        game_id = CustomParams.random_game_id().get('gameId')
        return {
            "userId": user_id,
            "gameId": game_id
        }

    @staticmethod
    def __random_user_id_and_game_ids():
        user_id = CustomParams.random_user_id().get('userId')
        total = random.randrange(1, 3)
        game_ids = []
        while total > 0:
            total = total - 1
            game_ids.append(CustomParams.random_game_id().get('gameId'))
        return {
            "userId": user_id,
            "gameIds": game_ids
        }

    @staticmethod
    def __random_user_id_and_user_ids():
        user_id = CustomParams.random_user_id().get('userId')
        total = random.randrange(1, 3)
        user_ids = []
        while total > 0:
            total = total - 1
            user_ids.append(CustomParams.random_user_id().get('userId'))
        return {
            "userId": user_id,
            "ids": user_ids
        }

    @staticmethod
    def random_user_id_list():
        total = random.randrange(1, 5)
        user_ids = []
        while total > 0:
            total = total - 1
            user_ids.append(CustomParams.random_user_id().get('userId'))
        return {"userIdList": user_ids}

    @staticmethod
    def random_user_ids():
        total = random.randrange(1, 5)
        user_ids = []
        while total > 0:
            total = total - 1
            user_ids.append(CustomParams.random_user_id().get('userId'))
        return {"userIds": user_ids}

    @staticmethod
    def random_sub_key():
        index = random.randrange(0, len(sub_key_list))
        return {"subKey": sub_key_list[index]}

    @staticmethod
    def random_rank_key():
        index = random.randrange(0, len(rank_key_list))
        return {"rankKey": rank_key_list[index]}

    @staticmethod
    def random_member_id_and_rank_key():
        user_id = CustomParams.random_user_id().get('userId')
        rank_key = CustomParams.random_rank_key().get("rankKey")
        return {"member": str(user_id), "key": rank_key}

    @staticmethod
    def random_rank_key_and_offset():
        rank_key = CustomParams.random_rank_key().get("rankKey")
        start = random.randrange(0, 1000)
        end = random.randrange(0, 1000)
        return {"key": rank_key, "start": min(start, end), "end": max(start, end)}
