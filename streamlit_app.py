import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    
    fig = px.bar(df, x='What is your age group?',
             title='Distribution of Age Groups',
             color_discrete_sequence=px.colors.qualitative.Set2)

    fig.update_layout(xaxis_title="Age Group",
                  yaxis_title="Count",
                  xaxis_tickangle=-45)
    st.plotly_chart(fig)

    movie_genre_counts = px.bar(df, x = 'Which one of the following genres do you prefer to watch? (Select your top most favorite)',title = 'Genre Count')

    movie_genre_counts.update_layout(
    xaxis_title='Genre',
    yaxis_title='Genre Count',
    title={
    'text': 'Satisfaction with Streaming Recommendations',
    'y': 0.9,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'},
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)
#st.plotly_chart(movie_genre_counts)

    fig = px.histogram(df,
                   x='How satisfied are you with the recommendations you receive from streaming platforms?',
                   nbins=4,
                   title='Satisfaction with Streaming Recommendations',
                   color_discrete_sequence=['coral'])

    fig.update_layout(xaxis_title='Satisfaction Level',
                  yaxis_title='Count',
                   title={
        'text': 'Satisfaction with Streaming Recommendations',
        'y': 0.9,  # Title position
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'yanchor': 'top'})
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

