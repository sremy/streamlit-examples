import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import ticker
from datetime import date, timedelta

st.set_page_config(layout="wide")


def main():

    df = fetch_contamination_data()
    st.title('Streamlit example')
    st.text('Hello')

    if st.checkbox('Show tail of dataframe'):
        # st.write(df.columns)
        st.write(df.tail(10))

    # Keep only positive regardless the age class
    df_by_day = df[df.cl_age90 == 0]

    plot_whole_positive(df_by_day)

    st.subheader('Zoom sur les n derniers jours')
    nb_days = st.slider('Select nb of days', value=30,  min_value=4, max_value=60)
    st.text('nb days: %i' % nb_days)

    # Compute the begin date according to the chosen nb_days
    begin_date = date.today() - timedelta(days=nb_days)
    st.write(f'Begin date: {begin_date}')
    df_by_day_latest = df_by_day[df_by_day.jour >= str(begin_date)]

    # Compute the cumulative positive count
    df_by_day_latest['P_cumul'] = df_by_day_latest.loc[:, 'P'].cumsum()

    plot_since_beginning(df_by_day_latest)


@st.cache
def fetch_contamination_data():
    data_file = 'C:/Users/Denis/Documents/seb/code/python/data/sp-pos-quot-fra-2022-01-30-19h09.csv'
    data_url = 'https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c'
    # Describe data
    df = pd.read_csv(data_url, sep=';', parse_dates=['jour'])
    return df


def plot_since_beginning(df_by_day_2022):
    from matplotlib.ticker import MultipleLocator, StrMethodFormatter, FuncFormatter
    plt.style.use('default')
    fig = plt.figure(figsize=(18, 5))
    fig.suptitle('Dataset Covid 19')
    ax = plt.axes()
    ax_right = ax.twinx()
    ax.set_title('Nombre de test positifs et cumul depuis le ' + df_by_day_2022.jour.iloc[0].strftime('%d/%m/%Y'))
    ax.bar(df_by_day_2022.jour, df_by_day_2022.P)
    ax_right.plot(df_by_day_2022.jour, df_by_day_2022.P_cumul, color='red')
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(50000))
    ax.grid(axis='y')
    ax_right.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%i M' % (x / 1000000)))
    ax_right.spines['right'].set_color('red')
    ax_right.tick_params(axis='y', colors='red')
    st.pyplot(fig)


def plot_whole_positive(df_by_day):
    plt.style.use('bmh')
    fig = plt.figure(figsize=(20, 6))
    ax = plt.axes()
    ax.set_title('Nombre de tests positifs depuis 2020')
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
    plt.bar(df_by_day.jour, df_by_day.P)
    # plt.show()
    st.pyplot(fig)


if __name__ == '__main__':
    main()
