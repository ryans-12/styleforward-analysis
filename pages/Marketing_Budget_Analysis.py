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


def display_marketing_spend_metric():
    st.metric(label = "Total Marketing Spend:  \n", value = "$8.2M", border = True)

def display_marketing_spend_vs_revenue_pie():
    
    spend = 8.2
    revenue = 185
    remaining = revenue - spend

    # Labels and data
    labels = ['$8.2M', '$185M']
    sizes = [spend, remaining]

    # Colors
    colors = ['#d92d3a', "#f3c5c9"]

    # Create pie chart
    fig, ax = plt.subplots(figsize = (3,3))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode = [0.12,0])
    ax.set_title('Percentage of Revenue spent on Marketing  \n', weight='bold')

    st.pyplot(fig)

def spend_vs_revenue_bar():
    marketing_spend = import_to_pandas('SELECT CAMPAIGN_ID, SUM(SPEND_AMOUNT) AS TOTAL_SPEND FROM MARKETING_SPEND GROUP BY CAMPAIGN_ID')
    marketing_budget = import_to_pandas('SELECT CAMPAIGN_ID, BUDGET FROM MARKETING_CAMPAIGNS')

    spend_and_budget = pd.merge(marketing_spend, marketing_budget, on = 'CAMPAIGN_ID', how = 'inner')

    #remove where 0 was spent
    spend_and_budget = spend_and_budget[spend_and_budget['TOTAL_SPEND'] >= 100]

    #sort by budget
    spend_and_budget = spend_and_budget.sort_values(by = 'BUDGET', ascending=False)
    # Set positions for bars
    ids = spend_and_budget['CAMPAIGN_ID']
    x = range(len(ids))  # positions for each id
    bar_width = 0.35

    # Create the plot
    fig, ax = plt.subplots()

    # Bars for budget and money spent
    ax.bar([pos - bar_width/2 for pos in x], spend_and_budget['TOTAL_SPEND'], width=bar_width, label='Total Spent', color='#d92d3a')
    ax.bar([pos + bar_width/2 for pos in x], spend_and_budget['BUDGET'], width=bar_width, label='Budget', color='#eb9098')

    # Customize chart
    ax.set_xticks(x)
    ax.set_xticklabels(ids)
    ax.set_xlabel('Campaign ID', fontsize = 12)
    ax.set_ylabel('Amount ($)', fontsize = 12)
    ax.set_title('Budget vs Money Spent per Campaign  \n', weight = 'bold')
    ax.legend()

    st.pyplot(fig, width = 'stretch')

def display_marketing_spend_bar():
    spend_by_channel = import_to_pandas('SELECT CHANNEL, SUM(SPEND_AMOUNT) AS TOTAL_SPEND_BY_CHANNEL FROM MARKETING_SPEND GROUP BY CHANNEL')
    spend_by_channel['TOTAL_SPEND_BY_CHANNEL']=spend_by_channel['TOTAL_SPEND_BY_CHANNEL'].astype(float)
    spend_by_channel = spend_by_channel.sort_values(by = 'TOTAL_SPEND_BY_CHANNEL', ascending=False)
    # Plotting
    fig, ax = plt.subplots()
    spend_by_channel.plot(x="CHANNEL", y="TOTAL_SPEND_BY_CHANNEL", kind="bar", color =  sns.color_palette(tjx_colors),legend=False, ax =ax)
    plt.title("Marketing Spend by Channel  \n", weight = 'bold')
    plt.xlabel("Channel", fontsize = 12)
    plt.ylabel("Spend in USD ($)", fontsize = 12)
    st.pyplot(fig, width= 'stretch')

def display_ROAS_bar():
    spend_df = import_to_pandas('SELECT CHANNEL, SUM(CLICKS) as TOTAL_CLICKS, SUM(SPEND_AMOUNT) AS TOTAL_SPEND, SUM(REVENUE_ATTRIBUTED) as TOTAL_REVENUE FROM MARKETING_SPEND GROUP BY CHANNEL')
    
    # Create scatter plot
    fig, ax = plt.subplots()
    ax.scatter(spend_df['TOTAL_SPEND'], spend_df['TOTAL_REVENUE'], color='#bd222e')

    
    # Annotate each point with its ID
    for i in range(len(spend_df)):
        ax.annotate(spend_df['CHANNEL'][i], (spend_df['TOTAL_SPEND'][i], spend_df['TOTAL_REVENUE'][i]),
                    textcoords="offset points", xytext=(5,5), ha='center')


    # Customize chart
    ax.set_title('Spending vs Revenue by Channel  \n', weight = 'bold')
    ax.set_xlabel('Total Spending ($)', fontsize = 12)
    ax.set_ylabel('Total Revenue ($)', fontsize = 12)

    st.pyplot(fig)

#OUTPUT ITEMS
st.markdown("<h1 style='text-align: center; color: #9C1C26;'>Marketing Budget Analysis</h1>", unsafe_allow_html=True)
row1 = st.columns(2, border= True)
r1c1 = row1[0]
r1c2 = row1[1]


row2 = st.columns(2, border = True)
r2c1 = row2[0]
r2c2 = row2[1]

with r1c1:
    display_marketing_spend_metric()
    display_marketing_spend_vs_revenue_pie()

with r1c2:
    display_marketing_spend_bar()
with r2c1:
    spend_vs_revenue_bar()

with r2c2:
    display_ROAS_bar()

    
    

