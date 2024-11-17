import numpy as np
import pandas as pd


def select_stratified_groups(data, strat_columns, group_size, weights=None, seed=None):
    """Подбирает стратифицированные группы для эксперимента.

    data - pd.DataFrame, датафрейм с описанием объектов, содержит атрибуты для стратификации.
    strat_columns - List[str], список названий столбцов, по которым нужно стратифицировать.
    group_size - int, размеры групп.
    weights - dict, словарь весов страт {strat: weight}, где strat - либо tuple значений элементов страт,
        например, для strat_columns=['os', 'gender', 'birth_year'] будет ('ios', 'man', 1992), либо просто строка/число.
        Если None, определить веса пропорционально доле страт в датафрейме data.
    seed - int, исходное состояние генератора случайных чисел для воспроизводимости
        результатов. Если None, то состояние генератора не устанавливается.

    return (data_pilot, data_control) - два датафрейма того же формата, что и data
        c пилотной и контрольной группами.
    """
    data=data.copy()
    rng = np.random.RandomState(seed)
    data_size = data.shape[0]
    data.reset_index(inplace=True)
    if not weights:
        weights = data.groupby(strat_columns)[list(set(data.columns)-set(strat_columns))[0]].count().to_dict()
        for key, value in weights.items():
            weights[key]=value/data_size
    
    strat_sizes = dict()
    for key, value in weights.items():
        strat_sizes[key]=round(value*group_size)
    strat_sizes

    strat_data = data.groupby(strat_columns).apply(lambda f: f.to_numpy())
    res_1 = pd.DataFrame()
    res_2 = pd.DataFrame()
    for key, value in strat_sizes.items():
        sample = strat_data[key][rng.choice(a = strat_data[key].shape[0], size=2*value, replace=False)]
        sample_1 = sample[:value]
        sample_2 = sample[value:]
        res_1 = pd.concat([res_1, pd.DataFrame(data = sample_1, columns= data.columns)])
        res_2 = pd.concat([res_2, pd.DataFrame(data = sample_2, columns= data.columns)])
    res_1.set_index('index', inplace=True)
    res_2.set_index('index', inplace=True)
    return res_1, res_2