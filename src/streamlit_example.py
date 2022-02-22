import streamlit as st
import pandas as pd


def main():
    st.title('Streamlit example')
    st.text('Hello')

    nb_days = st.slider('Select nb of days', min_value=0, max_value=30)
    st.text('nb days: %i' % nb_days)

    data = pd.DataFrame({'x': range(nb_days), 'y': range(0, 2*nb_days, 2)})
    if st.checkbox('Show dataframe'):
        st.write(data)

    st.line_chart(data)


if __name__ == '__main__':
    main()
