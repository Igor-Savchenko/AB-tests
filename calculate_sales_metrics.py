import pandas as pd


def calculate_sales_metrics(df, cost_name, date_name, sale_id_name, period, filters=None):
    """Вычисляет метрики по продажам.
    
    df - pd.DataFrame, датафрейм с данными. Пример
        pd.DataFrame(
            [[820, '2021-04-03', 1, 213]],
            columns=['cost', 'date', 'sale_id', 'shop_id']
        )
    cost_name - str, название столбца с стоимостью товара
    date_name - str, название столбца с датой покупки
    sale_id_name - str, название столбца с идентификатором покупки (в одной покупке может быть несколько товаров)
    period - dict, словарь с датами начала и конца периода пилота.
        Пример, {'begin': '2020-01-01', 'end': '2020-01-08'}.
        Дата начала периода входит в полуинтервал, а дата окончания нет,
        то есть '2020-01-01' <= date < '2020-01-08'.
    filters - dict, словарь с фильтрами. Ключ - название поля, по которому фильтруем, значение - список значений,
        которые нужно оставить. Например, {'user_id': [111, 123, 943]}.
        Если None, то фильтровать не нужно.

    return - pd.DataFrame, в индексах все даты из указанного периода отсортированные по возрастанию, 
        столбцы - метрики ['revenue', 'number_purchases', 'average_check', 'average_number_items'].
        Формат данных столбцов - float, формат данных индекса - datetime64[ns].
    """
    df[date_name]=pd.to_datetime(df[date_name])
    filtered_df = df
    if not(filters is None):
        for key, value in filters.items():
            filtered_df = filtered_df[filtered_df[key].isin(value)]

    filtered_df = filtered_df[(filtered_df[date_name]>=period['begin']) & (filtered_df[date_name]<period['end'])]
    sale_df = filtered_df.groupby(sale_id_name).agg(
        sale_cost = (cost_name, 'sum'),
        number_of_poisitions = (cost_name, 'count'),
        date = (date_name, 'min'))
    res = sale_df.groupby(date_name).agg(
        revenue = ('sale_cost', 'sum'),
        number_purchases = ('sale_cost', 'count'),
        average_check = ('sale_cost', 'mean'),
        average_number_items = ('number_of_poisitions', 'mean'))
    res = res.astype(float)
    res = res.sort_index(ascending=True)
    begin = pd.to_datetime(period['begin'])
    end = pd.to_datetime(period['end'])
    date = pd.to_datetime(begin)
    dates = []
    while date<end:
        dates.append(date)
        date = date + pd.DateOffset(days=1)
    result = res.join(pd.DataFrame(index=pd.Index(dates, name='date')),how = 'outer').fillna(0)
    return result