# -*- coding: utf-8 -*
import os
import sys
import getopt
sys.path.append('../')
from lib import ClearImage


# 清理类型（all、day）
c_type = 'all'
# 清理7日前的绘图
day = 7
file_path = '../image/'


def get_image_info(c, end_point=None):
    divisor = 1024
    if c == 'm' or c == 'mb' or c == 'M' or c == 'MB':
        divisor = divisor * divisor
    elif c == 'g' or c == 'gb' or c == 'G' or c == 'GB':
        divisor = divisor * divisor * divisor
    total_size = 0
    for root, dirs, files in os.walk(file_path):
        for f in files:
            if f.endswith(end_point):
                total_size += os.path.getsize(os.path.join(root, f))
    return "{:.3f}".format(total_size / divisor)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "t:d:i:", ['-t', '--type', '-d', '--day', '-i', '--info'])
    if len(sys.argv) == 1:
        clear_image = ClearImage()
        clear_image.do_clear(c_type, day)
        sys.exit(1)

    if sys.argv[1] in ('-i', '--info'):
        for opt, arg in opts:
            print('in calculation...')
            print('image occupied memory: ' + get_image_info(arg, '.png') + arg)
        sys.exit(1)
    if sys.argv[1] in ('-t', '--type', '-d', '--day'):
        for opt, arg in opts:
            if opt in ('-t', '--type'):
                c_type = arg
            if opt in ('-d', '--day'):
                day = int(arg)
    clear_image = ClearImage()
    clear_image.do_clear(c_type, day)
