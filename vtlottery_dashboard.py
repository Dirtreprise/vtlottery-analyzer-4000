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

    # Inspect and rename columns for consistency
    df.columns = df.columns.str.strip()
    
    # Ensure the columns needed exist, or rename accordingly
    expected_columns = ['Game Name', 'Price', 'Top Prize', 'Top Prizes Unclaimed', 'Total Unclaimed', 'Percent Sold', 'Tickets Printed']
    actual_columns = df.columns.tolist()

    # Check for key columns and rename if slightly different
    column_renames = {}
    for col in actual_columns:
        if 'Tickets Printed' in col:
            column_renames[col] = 'Tickets Printed'
        elif 'Total Unclaimed' in col:
            column_renames[col] = 'Total Unclaimed'
        elif 'Top Prizes Unclaimed' in col:
            column_renames[col] = 'Top Prizes Unclaimed'
    df = df.rename(columns=column_renames)

    # Clean up numeric columns (remove '$' and ',' and convert to numeric)
    df['Total Unclaimed'] = df['Total Unclaimed'].replace('[\$,]', '', regex=True).astype(float)
    df['Tickets Printed'] = df['Tickets Printed'].replace('[\$,]', '', regex=True).astype(float)

    # Calculate EV per ticket
    df['EV per Ticket'] = df['Total Unclaimed'] / df['Tickets Printed']

    return df

st.title("🎟️ Vermont Lottery Scratch Ticket Dashboard")

df = scrape_vtlottery()

# Display the dataframe sorted by EV per Ticket
st.dataframe(df.sort_values(by='EV per Ticket', ascending=False).reset_index(drop=True))
