import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_credentials():
        return st.secrets["GOOGLE_SHEETS_CREDS"]

def connect_to_google_sheets(user_data):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        creds_dict = load_credentials()
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open(user_data).sheet1
        
        return sheet

def load_data(sheet):
        data = sheet.get_all_records()
        return pd.DataFrame(data)

st.set_page_config(layout='wide')
ott=st.sidebar.selectbox('OTT Platform',['Home','Dashboard','Model1','Model2'])


def home():

    st.markdown("<h1 style='text-align: center;'>User collected responses: Google Data preview</h1>", unsafe_allow_html=True)
    SHEET_NAME = "user_data"
    sheet = connect_to_google_sheets(SHEET_NAME)
    df = load_data(sheet)
    st.write("Data from Google Sheets:")
        
    if 'Timestamp' in df.columns:
        df = df.drop('Timestamp', axis=1)

    df.rename(columns={'What is your age group?':'Age group',
                        'Which mode do you prefer to watch movies?': 'Preferred Mode',
                        'Which one of the following genres do you prefer to watch? (Select your top most favorite)': 'Favorite Genre',
                        'Which of the following do you use most frequently to choose a streaming platform?': 'Platform Choice Factor',
                        'On which devices do you primarily watch content?': 'Primary Device(to watch content)',
                        'How often do you watch or consume content from streaming platforms?': 'Watch Frequency',                 
                            'How satisfied are you with the recommendations you receive from streaming platforms?': 'Satisfaction Level',
                            'Are you satisfied with the recommendations you receive from streaming platforms?': 'Recommendation Satisfaction',
                            'What prevents you from using Netflix?': 'Netflix Barrier',
                            'How long do you spend each day watching content on streaming services?': 'Daily Watch Time',
                            'Does high subscription rate of one platform, forces you to switch to another platform?': 'Switching Due to Cost',
                            'Kindly give your preference':'Duration preference (season/hr wise)'},inplace=True)
        
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

def dashboard():

    SHEET_NAME = "user_data"
    sheet = connect_to_google_sheets(SHEET_NAME)
    df = load_data(sheet)

    st.markdown("<h1 style='text-align: center;'>Netflix Recommendation System Dashboard</h1>", unsafe_allow_html=True)
   
    if 'Timestamp' in df.columns:
        df = df.drop('Timestamp', axis=1)

    df.rename(columns={'What is your age group?':'Age group',
                       'Which mode do you prefer to watch movies?': 'Preferred Mode',
                       'Which one of the following genres do you prefer to watch? (Select your top most favorite)': 'Favorite Genre',
                       'Which of the following do you use most frequently to choose a streaming platform?': 'Platform Choice Factor',
                       'On which devices do you primarily watch content?': 'Primary Device(to watch content)',
                       'How often do you watch or consume content from streaming platforms?': 'Watch Frequency',                 
                        'How satisfied are you with the recommendations you receive from streaming platforms?': 'Satisfaction Level',
                        'Are you satisfied with the recommendations you receive from streaming platforms?': 'Recommendation Satisfaction',
                        'What prevents you from using Netflix?': 'Netflix Barrier',
                        'How long do you spend each day watching content on streaming services?': 'Daily Watch Time',
                        'Does high subscription rate of one platform, forces you to switch to another platform?': 'Switching Due to Cost',
                        'Kindly give your preference':'Duration preference (season/hr wise)'},inplace=True)
    
    column_values = df['Preferred Mode']
    column_values_list = df['Preferred Mode'].tolist()
    df['Preferred Mode'] = df['Preferred Mode'].str.split(' - ').str[0]

    col1, col2 = st.columns((10,10))
    
    fig1 = px.bar(
        df, 
        x='Preferred Mode',
        title = 'Preferred Watching mode',
        # color = 'Preferred Mode',
        color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig1.update_layout(
        xaxis_title='Preferred Watching Mode',
        yaxis_title='Count',
        title = {
            "text": 'Preferred Watching mode',
            "x": 0.3,
            'y': 0.9
        }
    )
    col1.plotly_chart(fig1)

    fig2 = px.box(df,
             x='Age group',
             y='Watch Frequency',
             title='Satisfaction Across Age Groups',
             color='Age group',
             color_discrete_sequence=px.colors.qualitative.Set2)

    fig2.update_layout(xaxis_title='Age Group', yaxis_title='Satisfaction Level',
                       title = {
                           "text": "Satisfaction Across Age Groups",
                           'x': 0.3
                       })
    col2.plotly_chart(fig2)
    
    fig3 = px.bar(df, x='Age group',
              title='Distribution of Age Groups',
              color = 'Age group',
              color_discrete_sequence=px.colors.qualitative.Set2)

    fig3.update_layout(xaxis_title="Age Group",
                  yaxis_title="Count",
                  #xaxis_tickangle=-45,
                  title = {
                           "text": "Satisfaction across Age Groups",
                           'x': 0.3
                       })
    col1.plotly_chart(fig3)

    fig4 = px.bar(df, x = 'Favorite Genre',title = 'Genre Count', color = 'Favorite Genre', color_discrete_sequence=px.colors.qualitative.Set2)
    fig4.update_layout(
    xaxis_title='Genre',
    yaxis_title='Genre Count',
    title={
    'text': 'User preferred Genres',
    'y': 0.9,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'}
   )
    col2.plotly_chart(fig4)

    fig5 = px.histogram(df,
                   x='Satisfaction Level',
                   nbins=4,
                   title='Satisfaction with Streaming Recommendations',
                #    color = 'Satisfaction Level',
                   color_discrete_sequence=px.colors.qualitative.Set2)

    fig5.update_layout(xaxis_title='Satisfaction Level',
                  yaxis_title='Count',
                   title={
        'text': 'Satisfaction with Streaming Recommendations',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    col1.plotly_chart(fig5)

if ott=='Home':
    home()
elif ott=='Dashboard':
     dashboard()