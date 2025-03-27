import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

@st.cache_data(ttl=86400)  # Data updates daily
def scrape_vtlottery():
    url = "https://vtlottery.com/games/instant-tickets/outstanding-prizes"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find("table")
    df = pd.read_html(str(table))[0]

    # Calculate EV per ticket (total prizes remaining / number of tickets)
    df['EV per Ticket'] = df['Total Unclaimed'] / df['# of Tickets']

    return df

st.title("Vermont Lottery Scratch Ticket Dashboard")
df = scrape_vtlottery()

# Display sortable table
st.dataframe(df.sort_values(by='EV per Ticket', ascending=False))