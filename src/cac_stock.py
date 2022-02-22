import copy

import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")


@st.cache
def load_cac():
    """ Fetch CAC composition from Wikipedia """
    url = "https://en.wikipedia.org/wiki/CAC_40"
    html = pd.read_html(url, match='Ticker')
    df_cac = html[0]

    return df_cac


def main():

    st.title('Streamlit & CAC')
    st.text('Composition du CAC 40 depuis Novembre 2021')
    df_cac = load_cac()
    df_cac = copy.deepcopy(df_cac)

    # Filter selected sectors
    sectors_list = sorted(df_cac['Sector'].unique())
    selected_sectors = st.sidebar.multiselect("Secteurs", sectors_list, default=sectors_list)
    df_filtered = df_cac[df_cac["Sector"].isin(selected_sectors)]
    st.subheader('Sociétés appartenant aux secteurs sélectionnés')
    st.write(f'{len(selected_sectors)} secteurs sélectionnés: {len(df_filtered)} sociétés')
    st.dataframe(df_filtered)

    big_df = fetch_stocks(list(df_cac.Ticker))
    print(big_df.index)
    print(big_df.columns)

    evolution = pd.Series(100 * big_df.iloc[-1, :].loc[:, 'Close'] / big_df.iloc[0, :].loc[:, 'Close'], name='Ticker')
    df_filtered = df_filtered.merge(pd.DataFrame({'Evolution (%)': evolution, 'Ticker': evolution.index}), on='Ticker')
    plot_history(big_df, list(df_filtered.Ticker))
    df_filtered

    plot_plotly(big_df, list(df_filtered.Ticker), df_cac)


def plot_history(df, tickers):

    fig = plt.figure(figsize=(20, 8))
    ax = plt.axes()
    ax.grid(axis='y')
    for ticker in tickers:
        plot_ticker(ax, df[ticker])

    st.pyplot(fig)


def plot_ticker(ax, df):
    ax.plot(df.index, 100 * df.Close / df.Close[0])


def plot_plotly(big_df, tickers, df_cac):
    import plotly.express as px
    import plotly.graph_objects as go

    fig = go.Figure({'layout': {'width': 1400, 'height': 800}})  # layout=go.Layout(height=800, width=1400)
    for ticker in tickers:
        df = big_df[ticker]
        df_company = df_cac[df_cac.Ticker == ticker]
        fig.add_trace(go.Scatter(x=df.index,
                                 y=100 * df.Close / df.Close[0],
                                 mode='lines', name=df_company.Company.iat[0]))

    st.plotly_chart(fig)


@st.cache
def fetch_stock(ticker):
    equity = yf.Ticker(ticker)

    print(equity.info)
    history = equity.history("1y", actions=False)
    print(history)
    return history


@st.cache
def fetch_stocks(tickers):
    """Return a dataframe with a hierarchical index"""
    big_df = yf.download(tickers, period="1y", interval="1d", actions=False, group_by='ticker')
    print(big_df)
    return big_df


if __name__ == '__main__':
    main()
