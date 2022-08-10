# -*- coding: utf-8 -*
import matplotlib
# agg类型为non-gui客户端
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.figure(figsize=(16, 8))
plt.title('WebPressure Data', fontsize=20)
plt.ylabel('Response Time(ms)', fontsize=18)
plt.xlabel('Request Times', fontsize=18)
plt.tick_params(labelsize=16)
import operator
import os
import json


__all__ = 'PerformanceDataPlot',


class PerformanceDataPlot:

    def __init__(self, s):
        self.__sequence_key = 'sequence'
        self.__sequence_json = 'sequence.json'
        self.__plot_name = '%s_%s.png'
        self.__base_dir = '../image/%s/' % s

    def data_plot(self, c, f, y):
        image_dir = self.__base_dir + c + '/' + f + '/'
        min_t = min(y)
        max_t = max(y)
        if len(y) - 2 > 100:
            base_count = int(len(y) / 100)
            count = 0
            total = 0
            new_y = []
            for d in y:
                if d == min_t or d == max_t:
                    new_y.append(d)
                    continue
                count = count + 1
                total = total + d
                if count == base_count:
                    new_y.append(float("{:.3f}".format(total / count)))
                    count = 0
                    total = 0
            y = new_y
        x = [i for i in range(1, len(y) + 1)]
        min_index, min_value = min(enumerate(y), key=operator.itemgetter(1))
        max_index, max_value = max(enumerate(y), key=operator.itemgetter(1))
        self.__point_line(x, y)
        plt.annotate(str(min_value), xy=(min_index + 1, min_value))
        plt.annotate(str(max_value), xy=(max_index + 1, max_value))
        self.save_image(f, image_dir)
        # GUI客户端展示，非GUI客户端则注释即可
        # plt.show()

    @staticmethod
    def __point_line(x, y, color='red', label=None):
        plt.plot(x, y, '.-', color=color, label=label)

    @staticmethod
    def __line(x, y, color='red', line_width=2, line_style='--'):
        plt.plot(x, y, color=color, linewidth=line_width, linestyle=line_style)

    def save_image(self, f, image_dir):
        sequence = 1
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            with open(image_dir + self.__sequence_json, 'w') as json_file:
                json.dump({self.__sequence_key: sequence}, json_file, indent=4)
        else:
            with open(image_dir + self.__sequence_json, 'r') as json_str:
                sequence = json.load(json_str).get(self.__sequence_key) + 1
            with open(image_dir + self.__sequence_json, 'w') as json_file:
                json.dump({self.__sequence_key: sequence}, json_file, indent=4)
        plt.savefig(image_dir + (self.__plot_name % (f, sequence)))
