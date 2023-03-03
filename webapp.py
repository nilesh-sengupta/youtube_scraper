import streamlit as st
import requests
import pandas as pd
import numpy as np


def readCSV():
    df = pd.read_csv('data.csv')
    df.drop(df.columns[0], axis=1, inplace=True)
    return df


st.title('Perceiving Public Sentiment through Social Media Analysis')

st.header('Search YouTube')

data = st.text_input('Search Term:')
if st.button('Search'):
    body = {'search_term': data}
    response = requests.post('http://0.0.0.0:5000/', json=body)
    print(response.status_code)

st.dataframe(readCSV())
