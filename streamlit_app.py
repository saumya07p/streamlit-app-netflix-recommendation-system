import streamlit as st
!pip install plotly
import plotly.express as px

st.title("Netflix Recommendation System")
st.text('You are my sunshine')


device_usage = px.bar(df, x = 'Which mode do you prefer to watch movies?')

device_usage.update_layout(xaxis_title='Device',
                           yaxis_title='Count')

device_usage.show()