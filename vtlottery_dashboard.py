import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

@st.cache_data(ttl=86400)
def scrape_vtlottery():
    url = "https://vtlottery.com/games/instant-tickets/outstanding-prizes"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find("table")
    df = pd.read_html(str(table))[0]

    return df

st.title("Vermont Lottery Scratch Ticket Dashboard")
df = scrape_vtlottery()

# Display column names to debug
st.write(df.columns.tolist())

# Display DataFrame for visual inspection
st.dataframe(df)
