# -*- coding: utf-8 -*
import os
import time
import shutil

__all__ = 'ClearImage',


class ClearImage:

    def __init__(self):
        self.__base_image_dir = '../image/'

    def do_clear(self, c_type, day):
        if c_type == 'all':
            self.__clear_all()
            print('clear all image finish.')
        elif c_type == 'day':
            self.__clear_day(day)
            print('clear day image finish.')

    def __clear_all(self):
        shutil.rmtree(self.__base_image_dir)

    def __clear_day(self, d):
        file_list = self.__walk_files(self.__base_image_dir, '.png')
        judge_time = JudgeTime()
        del_file_list = []
        for f in file_list:
            if judge_time.judge(os.path.getctime(f), d):
                del_file_list.append(f)
        for d in del_file_list:
            os.remove(d)

    @staticmethod
    def __walk_files(path, endpoint=None):
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(endpoint):
                    file_list.append(file_path)
        return file_list


class JudgeTime:

    @staticmethod
    def judge(t, d):
        n_time = time.time()  # 获取当前时间
        result = n_time - t
        hour = result / 1000 / 60 / 60
        if hour < d * 24:
            return True
        else:
            return False
