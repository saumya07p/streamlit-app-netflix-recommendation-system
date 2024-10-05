import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from pathlib import Path

st.title("Netflix Recommendation System")
st.title("Google Sheets Data Dashboard")

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR88GrAY-eMPSXwVXOwoEABuu2z7D2cRGA58tfZLvCkbskX8zVzpmRQnuK2z5PHL7H9zJ2n4VK7fE4w/pub?gid=2145904198&single=true&output=csv"

data = pd.read_csv(url)

st.subheader("Data Preview")
st.dataframe(data)


st.page_link("streamlit_app.py", label="Home", icon="🏠")