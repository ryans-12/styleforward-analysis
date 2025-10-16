import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from data.snowflake_conn import import_to_pandas


transactions_df = import_to_pandas("SELECT * FROM transactions")

def display_total_sales():
    transactions_df["ORDER_DATE"] = pd.to_datetime(transactions_df["ORDER_DATE"], format='%m/%d/%y %H:%M', errors='coerce').dt.date

    min_date = transactions_df['ORDER_DATE'].min()
    min_date = min_date.strftime("%m/%d/%Y")
    max_date = transactions_df['ORDER_DATE'].max()
    max_date = max_date.strftime("%m/%d/%Y")
    total_sales = transactions_df['TOTAL_AMOUNT'].sum()
    total_sales = f"{total_sales}"
    st.metric(label = "Total Sales  \n" + min_date + " - " + max_date, value = "$" + total_sales, border = True)

def display_channel_pie():
    
    # Count frequency of each channel
    channel_counts = transactions_df['CHANNEL'].value_counts()
    channel_counts.columns = ['CHANNEL', 'COUNT']
    
    
    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(channel_counts, labels=channel_counts.index, autopct='%1.1f%%',textprops={'fontsize': 20}, colors = sns.color_palette('Reds'),startangle=90)
    ax.set_title('Sales by Channel', fontsize=32, weight='bold')
    st.pyplot(fig, width = "stretch")




#OUTPUT ITEMS
st.markdown("<h1 style='text-align: center; color: black;'>Executive Summary</h1>", unsafe_allow_html=True)
row1 = st.columns(3)
r1c1 = row1[0]
r1c2 = row1[1]
r1c3 = row1[2]

row2 = st.columns(2)
r2c1 = row2[0]
r2c2 = row2[1]


col1, col2, col3 = st.columns(3)


with r1c1:
    display_total_sales()

with r1c2:
    display_channel_pie()

st.text("")
st.text("")
with r2c1:
    display_channel_pie()


