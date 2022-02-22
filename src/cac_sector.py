import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


@st.cache
def load_cac():
    """ Fetch CAC composition from Wikipedia """
    url = "https://fr.wikipedia.org/wiki/CAC_40#Composition_actuelle"
    html = pd.read_html(url, match='Entrée dans l\'indice')
    df_cac = html[0]
    df_cac.iloc[:, 2] = df_cac.iloc[:, 2] / 100.0
    return df_cac


def main():
    st.set_page_config(layout="wide")
    st.title('Streamlit & CAC')
    st.text('Composition du CAC 40')
    df_cac = load_cac()
    df_cac

    # Plot pie chart
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    fig.set_figheight(8)
    ax.pie(df_cac.iloc[:, 2],
           labels=df_cac.iloc[:, 0], radius=0.45, labeldistance=1.1, rotatelabels=True, textprops={'size': 6})
    st.pyplot(fig)

    # Filter selected sectors
    sectors_list = sorted(df_cac['Secteur'].unique())
    selected_sectors = st.sidebar.multiselect("Secteurs", sectors_list, default=sectors_list)
    df_filtered = df_cac[df_cac["Secteur"].isin(selected_sectors)]
    st.header('Sociétés appartenant aux secteurs sélectionnés')
    st.write(f'{len(selected_sectors)} secteurs sélectionnés: {len(df_filtered)} sociétés')
    st.dataframe(df_filtered)


if __name__ == '__main__':
    main()
