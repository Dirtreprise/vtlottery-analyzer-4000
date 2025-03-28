import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://vtlottery.com/games/instant-tickets/outstanding-prizes"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find("table")
df = pd.read_html(str(table))[0]

# Replace these two column names exactly as shown in your dashboard:
total_unclaimed_col = 'TOTAL UNCLAIMED'   # <-- edit if different
tickets_printed_col = '# OF TICKETS'   # <-- edit if different

# Cleaning the data to ensure calculations work correctly:
df[total_unclaimed_col] = df[total_unclaimed_col].replace('[\$,]', '', regex=True).astype(float)
df[tickets_printed_col] = df[tickets_printed_col].replace('[\$,]', '', regex=True).astype(float)

# EV calculation:
df['EV per Ticket'] = df[total_unclaimed_col] / df[tickets_printed_col]

st.title("🎟️ VT Scratch Ticket Analyzer 4000")
st.dataframe(df.sort_values(by='EV per Ticket', ascending=False).reset_index(drop=True))
