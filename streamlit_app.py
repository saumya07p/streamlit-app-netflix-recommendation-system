import streamlit as st
import pandas as pd
import math
from pathlib import Path
import pandas as pd
import json


st.title("Netflix Recommendation System")
st.title("Load Google Sheet as CSV")

# Google Sheets published CSV URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR88GrAY-eMPSXwVXOwoEABuu2z7D2cRGA58tfZLvCkbskX8zVzpmRQnuK2z5PHL7H9zJ2n4VK7fE4w/pub?gid=2145904198&single=true&output=csv"  # Replace with your URL

# Load the CSV file
data = pd.read_csv(url)

# Display the data
st.subheader("Data Preview")
st.dataframe(data)