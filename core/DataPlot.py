import matplotlib.pyplot as plt
import operator

__all__ = 'PerformanceDataPlot',


class PerformanceDataPlot:

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
            plt.text(a, b + 2, int(b), ha=ha, va=va)
        plt.show()
