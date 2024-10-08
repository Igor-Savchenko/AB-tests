import numpy as np


def get_bernoulli_confidence_interval(values: np.array):
    """Вычисляет доверительный интервал для параметра распределения Бернулли.

    :param values: массив элементов из нулей и единиц.
    :return (left_bound, right_bound): границы доверительного интервала.
    """
    k = values.sum()
    n = values.shape[0]
    h = k/n
    d = 1.96*np.sqrt(h*(1-h)/n)
    left_bound = h - d
    right_bound = h + d
    if left_bound<0:
        left_bound = 0
    if right_bound<0:
        right_bound = 0
    if left_bound>1:
        left_bound = 1
    if right_bound>1:
        right_bound = 1    
    return (left_bound, right_bound)