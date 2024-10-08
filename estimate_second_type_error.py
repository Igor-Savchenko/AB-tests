import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

def check_ttest(a, b, alpha=0.05):
    """Тест Стьюдента. Возвращает 1, если отличия значимы."""
    _, pvalue = ttest_ind(a, b)
    return int(pvalue < alpha)

def estimate_second_type_error(df_pilot_group, df_control_group, metric_name, effects, alpha=0.05, n_iter=10000, seed=None):
    """Оцениваем ошибки второго рода.

    Бутстрепим выборки из пилотной и контрольной групп тех же размеров, добавляем эффект к пилотной группе,
    считаем долю случаев без значимых отличий.
    
    df_pilot_group - pd.DataFrame, датафрейм с данными пилотной группы
    df_control_group - pd.DataFrame, датафрейм с данными контрольной группы
    metric_name - str, названия столбца с метрикой
    effects - List[float], список размеров эффектов ([1.03] - увеличение на 3%).
    alpha - float, уровень значимости для статтеста
    n_iter - int, кол-во итераций бутстрапа
    seed - int or None, состояние генератора случайных чисел

    return - dict, {размер_эффекта: ошибка_второго_рода}
    """
    pilot_group_bootstrap = np.random.choice(df_pilot_group[metric_name], size=(n_iter, df_pilot_group[metric_name].shape[0]))
    control_group_bootstrap = np.random.choice(df_control_group[metric_name], size=(n_iter, df_control_group[metric_name].shape[0]))
    result = {}
    for effect in effects:
        res = 1-np.sum([check_ttest(a,b,alpha=alpha) for a,b in zip(pilot_group_bootstrap*effect, control_group_bootstrap)])/n_iter
        result[effect]=res
    return result 