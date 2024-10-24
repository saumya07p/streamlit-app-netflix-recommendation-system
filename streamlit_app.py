import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.title("Netflix Recommendation System")
st.text('You are my sunshine')

fig = px.bar(x=['A', 'B', 'C'], y=[10, 20, 30], title="Simple Bar Chart")
st.plotly_chart(fig)