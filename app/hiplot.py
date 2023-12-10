import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import hiplot as hip


sns.set_theme()

st.title('Sales Data Journey')

data = pd.read_csv('../data/data.csv', index_col=0)
# data.head()
stores = pd.read_csv('../data/stores.csv', index_col=0)
# stores.head()

# parallel coordinates
with st.container():
    q = data.copy()

    # normalize 0-1 each product family
    # q = q.pivot_table(values='sales', index=['date'], columns=['store_nbr', 'family'], aggfunc=np.mean)
    # q = q/q.max().values  # normalized to 0-1

    # # unpivot
    # q = q.reset_index()
    # q = pd.melt(q, id_vars='date', var_name=['store_nbr', 'family'], value_name='sales')
    # print(q.shape)

    # add attributes
    q = pd.merge(q, stores.reset_index(), on='store_nbr', how='inner')
    print(q.shape)

    # add holidays
    # h = holidays.copy()
    # h = h.groupby('date')['type'].agg(['count', list]).reset_index()
    # h['list'] = h['list'].apply(lambda x: '.'.join(map(str, list(set(x)))))
    # h.rename(columns={'list': 'holiday'}, inplace=True)

    # q = pd.merge(q, h, on='date', how='left')
    # q['holiday'].fillna('-', inplace=True)
    # print(q.shape)
    # display(q.head())

    q['date'] = pd.to_datetime(q['date'])
    q['month'] = q['date'].dt.month
    q['week'] = q['date'].dt.isocalendar().week
    q['year'] = q['date'].dt.year
    q['weekday'] = q['date'].dt.day_name()  #.weekday+1

    # q = q.pivot_table(values='sales', index=['type', 'store_nbr', 'month', 'week', 'family'], columns=['weekday'], aggfunc=np.sum)
    q = q.pivot_table(values='sales', index=['type', 'store_nbr', 'month', 'family'], aggfunc='mean')
        
    q.reset_index(inplace=True)
    # display(q.head())
    print(q.shape)

    
    xp = hip.Experiment.from_dataframe(q)
    xp.display_data(hip.Displays.PARALLEL_PLOT).update({
        'order': [
            'type', 'store_nbr', 'family', 
            'sales', 'month'][::-1],
    })
    xp.display_data(hip.Displays.TABLE).update({
        'hide': ['uid', 'from_uid'],
        # 'order_by': [['imdb']],
        # 'order': ['title'],
    })
    # xp.display()
    xp.to_streamlit().display()