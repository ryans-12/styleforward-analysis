
import streamlit as st
import pandas as pd
from data.snowflake_conn import import_to_pandas

st.title("📊 Data Explorer")

# Example data
df = import_to_pandas("Select * FROM Customer_Touchpoints")

st.dataframe(df)
