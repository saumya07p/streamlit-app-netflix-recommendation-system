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
    SHEET_NAME = "user_data"
    sheet = connect_to_google_sheets(SHEET_NAME)
    df = load_data(sheet)
    st.write("Data from Google Sheets:")
    
    if 'Timestamp' in df.columns:
        df = df.drop('Timestamp', axis=1)

    df.reset_index(drop=True, inplace=True)
       
    st.dataframe(df)
    columns_to_keep = st.multiselect("Select columns to keep:",options=df.columns)

    if columns_to_keep:
        df_filtered = df[columns_to_keep].copy()
        df_filtered.reset_index(drop=True, inplace=True)

        st.write("Selected column(s):")
        st.write(df_filtered)
    else:
        st.write("No columns selected.")
        
if __name__ == "__main__":
    main()