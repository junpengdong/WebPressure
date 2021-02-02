import matplotlib.pyplot as plt
import operator

__all__ = 'PerformanceDataPlot', 'PerformanceDataHandle',


class PerformanceDataHandle:

    def show_type_dispatch(self, data_arr, show_type='low'):
        if show_type == 'low':
            return self.low_handle(data_arr)
        elif show_type == 'medium':
            return self.medium_handle(data_arr)
        elif show_type == 'high':
            return self.high_handle(data_arr)

    @staticmethod
    def low_handle(data_arr):
        x = ['Min', 'Avg', 'Max']
        y = [min(data_arr), sum(data_arr) / len(data_arr), max(data_arr)]
        return x, y

    @staticmethod
    def medium_handle(data_arr):
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
    def high_handle(data_arr):
        y = [data_arr for data_arr in range(1, len(data_arr) + 1)]
        return data_arr, y


class PerformanceDataPlot:

    def __init__(self):
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # plt.figure(figsize=(16, 8))
        plt.title('WebPressure Data', fontsize=20)
        plt.ylabel('Response Time(ms)', fontsize=18)
        plt.xlabel('X label Describe', fontsize=18)
        plt.tick_params(labelsize=16)

    def data_plot_dispatch(self, x, y, show_type='bar'):
        if show_type == 'bar':
            self.bar(x, y)
        elif show_type == 'line':
            self.line(x, y)

    @staticmethod
    def line(x, y, color='red', line_width=2, line_style='--'):
        min_index, min_value = min(enumerate(y), key=operator.itemgetter(1))
        max_index, max_value = max(enumerate(y), key=operator.itemgetter(1))
        plt.plot(x, y, color, linewidth=line_width, linestyle=line_style)
        plt.annotate(str(min_value), xy=(min_index + 1, min_value))
        plt.annotate(str(max_value), xy=(max_index + 1, max_value))
        plt.show()

    @staticmethod
    def bar(x, y, ha='center', va='top'):
        plt.bar(x, y)
        for a, b in zip(x, y):
            plt.text(a, b + 25, int(b), ha=ha, va=va)
        plt.show()
