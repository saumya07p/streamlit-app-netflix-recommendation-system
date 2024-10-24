import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

st.title("Netflix Recommendation System")
st.text('You are my sunshine')
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import os

# Function to load credentials from Streamlit secrets
def load_credentials():
    creds_json = st.secrets["GOOGLE_SHEETS_CREDS"]
    return json.loads(creds_json)

# Function to authorize and connect to Google Sheets
def connect_to_google_sheets(user_data):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Load credentials from Streamlit secrets
    creds_dict = load_credentials()

    # Create credentials object
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    # Authorize client
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(user_data).sheet1

    return sheet

# Function to read data into a DataFrame
def load_data(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Streamlit app main function
def main():
    st.title("Google Sheets Data Viewer")
    
    # Replace with your actual Google Sheets name
    SHEET_NAME = "Project R&D (Responses)"
    
    # Connect to the Google Sheets
    try:
        sheet = connect_to_google_sheets(SHEET_NAME)
        df = load_data(sheet)
        
        st.write("Data from Google Sheets:")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")

if __name__ == "__main__":
    main()


fig = px.bar(x=['A', 'B', 'C'], y=[10, 20, 30], title="Simple Bar Chart")
st.plotly_chart(fig)