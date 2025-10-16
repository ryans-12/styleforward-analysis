
import streamlit as st
import pandas as pd

st.title("📊 Data Explorer")

# Example data
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 90, 78]
})

st.dataframe(df)
