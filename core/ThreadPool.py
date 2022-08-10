# -*- coding: utf-8 -*
from threading import Thread

__all__ = 'CustomThreadPool',


class CustomThreadPool(Thread):

    req_time_arr = []
    req_count_arr = []
    req_error_arr = []

    def __init__(self, func, args):
        super(CustomThreadPool, self).__init__()
        self.func = func
        self.args = args
        self.req_time_arr = []
        self.req_count_arr = []
        self.req_error_arr = []
        self.thread_arr = []
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            print(e)
            return None
