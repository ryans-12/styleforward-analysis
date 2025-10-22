import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
from data.snowflake_conn import import_to_pandas



st.set_page_config(
    layout="wide",
)

with open('pages/style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

tjx_colors = ['#9C1C26', '#bd222e', '#d92d3a', '#df4e59', '#e56f78', '#eb9098', '#f1b2b7']

def display_yearly_revenue():
    st.metric(label = "Yearly Revenue  \n", value = '$185M', delta="-10%", border = True)

def display_instore_vs_online_pie():
    instore = 129.5
    online = 55.5

    # Labels and data
    labels = ['Online ($55.5M)', 'In-Store ($129.5M)']
    sizes = [online, instore]

    # Colors
    colors = ['#d92d3a', "#f3c5c9"]

    # Create pie chart
    fig, ax = plt.subplots(figsize = (3,3))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.set_title('In Store vs Online Revenue  \n', weight='bold')

    st.pyplot(fig)

def display_store_count():
    st.metric(label = "Physical Store Count  \n", value = '47', border = True)


def display_foot_traffic():
    st.metric(label = "Foot Traffic (Customers/Day)  \n", value = '148.6', delta="-15%", border = True)

def display_sales_by_channel():
    transactions_df = import_to_pandas('SELECT CHANNEL, SUM(TOTAL_AMOUNT) as TOTAL_AMT FROM TRANSACTIONS GROUP BY CHANNEL')
    transactions_df['TOTAL_AMT']=transactions_df['TOTAL_AMT'].astype(float)

    transactions_df = transactions_df.sort_values(by = 'TOTAL_AMT', ascending=False)
    # Plotting
    fig, ax = plt.subplots(figsize = (4,2.5))
    transactions_df.plot(x="CHANNEL", y="TOTAL_AMT", kind="bar", color =  sns.color_palette(tjx_colors),legend=False, ax =ax)
    plt.title("Total Sales", weight = 'bold')
    plt.xlabel("", fontsize = 1)
    plt.ylabel("Total Sales ($)", fontsize = 10)
    plt.xticks(size = 8)
    plt.yticks(size = 8)
    st.pyplot(fig, width = 'stretch')


def promo_code_bar():
    promo_comp_df = import_to_pandas('SELECT PROMO_CODE_USED, TOTAL_AMOUNT FROM TRANSACTIONS')
    
    promo_comp_df['Promo Used'] = promo_comp_df['PROMO_CODE_USED'].notnull()
    avg_purchase = promo_comp_df.groupby('Promo Used')['TOTAL_AMOUNT'].mean()

    # Plot the result
    fig, ax = plt.subplots(figsize = (4,3))
    colors = ['#e56f78','#d92d3a']
    labels = ['No Promo', 'Promo Used']
    ax.bar(labels, avg_purchase.values, color=colors)
    ax.set_title('Impact of Promo Codes on Average Order Value', weight = 'bold')
    ax.set_ylabel('Average Total Amount ($)')

    st.pyplot(fig)


#OUTPUT ITEMS
st.markdown("<h1 style='text-align: center; color: #9C1C26;'>Sales Analysis</h1>", unsafe_allow_html=True)
col1, col2= st.columns([2,3], border= True)

with col1:
    display_yearly_revenue()
    display_instore_vs_online_pie()
    display_store_count()
    display_foot_traffic()

with col2:
    display_sales_by_channel()
    promo_code_bar()
    
