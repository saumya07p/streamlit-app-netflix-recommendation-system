import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials


st.title("Google Dataset preview")

def load_credentials():
    return st.secrets["GOOGLE_SHEETS_CREDS"]

def connect_to_google_sheets(user_data):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds_dict = load_credentials()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(user_data).sheet1
    
    return sheet

def load_data(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def main():
    st.title("Google Sheets Data Viewer")
    SHEET_NAME = "user_data"
    sheet = connect_to_google_sheets(SHEET_NAME)
    df = load_data(sheet)
    df.drop(['Timestamp'], axis = 1)
    st.write("Data from Google Sheets:")
    st.dataframe(df)

if __name__ == "__main__":
    main()