import matplotlib.pyplot as plt
import operator

__all__ = 'PerformanceDataPlot', 'PerformanceDataHandle',


class PerformanceDataHandle:

    def show_type_dispatch(self, data_arr, show_type='low'):
        if show_type == 'low':
            return self.__low_handle(data_arr)
        elif show_type == 'medium':
            return self.__medium_handle(data_arr)
        elif show_type == 'high':
            return self.__high_handle(data_arr)

    @staticmethod
    def __low_handle(data_arr):
        x = ['Min', 'Avg', 'Max']
        y = [min(data_arr), sum(data_arr) / len(data_arr), max(data_arr)]
        return x, y

    @staticmethod
    def __medium_handle(data_arr):
        if len(data_arr) < 50:
            y = [data_arr for data_arr in (1, len(data_arr) + 1)]
            return data_arr, y
        else:
            x_data = 1
            add_up = 0
            total_data = 0
            x = []
            y = []
            for data in data_arr:
                add_up = add_up + 1
                total_data = total_data + data
                if add_up == 10:
                    y.append(float("{:.3f}".format(total_data / add_up)))
                    x.append(x_data)
                    x_data = x_data + 1
                    add_up = 0
                    total_data = 0
            if total_data != 0:
                y.append(float("{:.3f}".format(total_data / add_up)))
                x.append(x_data)
            return x, y

    @staticmethod
    def __high_handle(data_arr):
        y = [data_arr for data_arr in range(1, len(data_arr) + 1)]
        return data_arr, y


class PerformanceDataPlot:

    def __init__(self):
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # plt.figure(figsize=(16, 8))
        plt.title('WebPressure Data', fontsize=20)
        plt.ylabel('Response Time(ms)', fontsize=18)
        # plt.xlabel('X label Describe', fontsize=18)
        plt.tick_params(labelsize=16)

    def data_plot_dispatch(self, x, y, show_type='bar'):
        if show_type == 'bar':
            self.__bar(x, y)
        elif show_type == 'line':
            self.__line(x, y)
        elif show_type == 'point_line':
            self.__point_line(x, y)
        plt.show()

    @staticmethod
    def __line(x, y, color='red', line_width=2, line_style='--'):
        min_index, min_value = min(enumerate(y), key=operator.itemgetter(1))
        max_index, max_value = max(enumerate(y), key=operator.itemgetter(1))
        plt.plot(x, y, color=color, linewidth=line_width, linestyle=line_style)
        plt.annotate(str(min_value), xy=(min_index + 1, min_value))
        plt.annotate(str(max_value), xy=(max_index + 1, max_value))

    @staticmethod
    def __bar(x, y, ha='center', va='top', color='red'):
        plt.bar(x, y, color=color)
        for a, b in zip(x, y):
            plt.text(a, b + 25, int(b), ha=ha, va=va)

    @staticmethod
    def __point_line(x, y, color='red', label=None):
        plt.plot(x, y, '.-', color=color, label=label)
