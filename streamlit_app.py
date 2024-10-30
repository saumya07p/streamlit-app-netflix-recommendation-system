import streamlit as st
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.title("Netflix Recommendation System Dashboard")

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
        
    st.write("Data from Google Sheets:")
    st.dataframe(df)

    num_rows, num_cols = df.shape
    st.write(f"Number of Rows: {num_rows}")
    st.write(f"Number of Columns: {num_cols}")

    device_usage = px.bar(df, x = 'Which mode do you prefer to watch movies?')
    device_usage.update_layout(xaxis_title='Device', yaxis_title='Count')
    st.plotly_chart(device_usage)
    
    fig = px.box(df,
             x='What is your age group?',
             y='How satisfied are you with the recommendations you receive from streaming platforms?',
             title='Satisfaction Across Age Groups',
             color='What is your age group?',
             color_discrete_sequence=px.colors.qualitative.Set2)

    fig.update_layout(xaxis_title='Age Group', yaxis_title='Satisfaction Level')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

