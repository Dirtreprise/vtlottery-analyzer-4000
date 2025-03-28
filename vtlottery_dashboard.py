import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://vtlottery.com/games/instant-tickets/outstanding-prizes"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find("table")
df = pd.read_html(str(table))[0]

st.title("Vermont Lottery Scratch Ticket Dashboard")
st.write("Here are the columns available:")
st.write(df.columns.tolist())  # This will show you exactly what columns are available
st.dataframe(df)
