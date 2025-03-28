import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://vtlottery.com/games/instant-tickets/outstanding-prizes"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find("table")
df = pd.read_html(str(table))[0]

# Clearly show column names:
st.write("Column names:", df.columns.tolist())
st.dataframe(df)
