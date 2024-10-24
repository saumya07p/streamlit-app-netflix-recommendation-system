import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

st.title("Netflix Recommendation System")
st.text('You are my sunshine')
from google.colab import drive
import json

drive.mount('/content/drive')
file_path = '/content/drive/My Drive/netflix-recommendation-system-19d21e28b1f4.json'

with open(file_path, 'r') as f:
    data = json.load(f)

print(data)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
client = gspread.authorize(creds)

sheet = client.open("Project R&D (Responses)").sheet1

data = sheet.get_all_records()

df = pd.DataFrame(data)

print(df)


fig = px.bar(x=['A', 'B', 'C'], y=[10, 20, 30], title="Simple Bar Chart")
st.plotly_chart(fig)