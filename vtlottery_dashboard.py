import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Adding the image
st.image("https://raw.githubusercontent.com/dirtreprise/vtlottery-dashboard/main/lotto.jpeg", use_column_width=True)

st.title("🎟️ VT Scratch Ticket Analyzer 4000")

# existing script below here...
url = "https://vtlottery.com/games/instant-tickets/outstanding-prizes"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find("table")
df = pd.read_html(str(table))[0]

total_unclaimed_col = 'Total Unclaimed'
tickets_printed_col = '# Of Tickets'
percent_sold_col = '% Sold'

df[total_unclaimed_col] = df[total_unclaimed_col].replace('[\$,]', '', regex=True).astype(float)
df[tickets_printed_col] = df[tickets_printed_col].replace('[\$,]', '', regex=True).astype(float)
df[percent_sold_col] = df[percent_sold_col].replace('%', '', regex=True).astype(float)

df['Remaining Tickets'] = df[tickets_printed_col] * (1 - (df[percent_sold_col] / 100))
df['EV per Remaining Ticket'] = df[total_unclaimed_col] / df['Remaining Tickets']

st.dataframe(df.sort_values(by='EV per Remaining Ticket', ascending=False).reset_index(drop=True))
