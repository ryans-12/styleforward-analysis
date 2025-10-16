import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
from data.snowflake_conn import import_to_pandas

st.set_page_config(
    layout="wide",
)


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

transactions_joined_stores = import_to_pandas("SELECT transactions.TRANSACTION_ID, transactions.STORE_ID, Stores.City, Stores.State, transactions.TOTAL_AMOUNT from transactions INNER JOIN Stores on Transactions.STORE_ID = Stores.Store_Id")

def display_stores_map():
    total_sales_by_store = transactions_joined_stores.groupby(['STORE_ID', 'CITY','STATE'])['TOTAL_AMOUNT'].sum().reset_index()
    # Rename the column for clarity
    total_sales_by_store.rename(columns={'TOTAL_AMOUNT': 'TOTAL_SALES'}, inplace=True)

    
    # Dictionary of coordinates keyed by city name
    coordinates = {
        'Austin': {'lat': 30.2711286, 'lon': -97.7436995},
        'Dallas': {'lat': 32.7762719, 'lon': -96.7968559},
        'Houston': {'lat': 29.7589382, 'lon': -95.3676974},
        'San Antonio': {'lat': 29.4246002, 'lon': -98.4951405},
        'Fort Worth': {'lat': 32.753177, 'lon': -97.3327459},
        'El Paso': {'lat': 31.7601164, 'lon': -106.4870404},
        'Plano': {'lat': 33.0136764, 'lon': -96.6925096},
    }

    
    # Map coordinates to the DataFrame
    total_sales_by_store['latitude'] = total_sales_by_store['CITY'].map(lambda city: coordinates[city]['lat'])
    total_sales_by_store['longitude'] = total_sales_by_store['CITY'].map(lambda city: coordinates[city]['lon'])

    total_sales_by_store['TOTAL_SALES'] = total_sales_by_store['TOTAL_SALES'].astype(float)

   # Create scatter map
    fig = px.scatter_map(
        total_sales_by_store,
        lat="latitude",
        lon="longitude",
        size="TOTAL_SALES",
        hover_name="CITY",
        hover_data={"STATE": True, "TOTAL_SALES": True},
        color_discrete_sequence=["red"],
        zoom=4,
        height=400
    )

    fig.update_layout(mapbox_style="MapboxBasic")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)




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
    display_stores_map()


