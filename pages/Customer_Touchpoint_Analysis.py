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

transactions_df = import_to_pandas("SELECT * FROM transactions")

#create data for pie charts for first and last touchpoints
touchpoints_df = import_to_pandas("SELECT * FROM customer_touchpoints")
#rename direct channel to website
touchpoints_df['CHANNEL'] = touchpoints_df['CHANNEL'].replace('Direct', 'Website')

touchpoints_df['interaction_datetime_parsed'] = pd.to_datetime(touchpoints_df['TOUCHPOINT_TIMESTAMP'], format='%m/%d/%y %H:%M', errors='coerce')
customer_touchpoints = touchpoints_df.sort_values(['CUSTOMER_ID', 'interaction_datetime_parsed'])
first_touch = customer_touchpoints.groupby('CUSTOMER_ID').first()[['CHANNEL', 'interaction_datetime_parsed']].rename(columns={'CHANNEL': 'first_touch_channel', 'interaction_datetime_parsed':'first_touch_time'})
last_touch = customer_touchpoints.groupby('CUSTOMER_ID').last()[['CHANNEL','interaction_datetime_parsed','CART_VALUE','TRANSACTION_ID','CONVERTED_FLAG']].rename(columns={'CHANNEL': 'last_touch_channel', 'interaction_datetime_parsed':'last_touch_time'})
attribution_df = first_touch.merge(last_touch, on='CUSTOMER_ID', how = 'outer')
attribution_df['channel_switch'] = attribution_df['first_touch_time'] != attribution_df['last_touch_time']
joined_df = attribution_df.merge(transactions_df[['TRANSACTION_ID', 'SUBTOTAL']], on = 'TRANSACTION_ID')
# Calculate percentage of appearance for each channel
first_touch_pct = joined_df['first_touch_channel'].value_counts(normalize=True) * 100
last_touch_pct = joined_df['last_touch_channel'].value_counts(normalize=True) * 100
# Combine into a single DataFrame
channel_stats = pd.DataFrame({
    'first_touch_pct': first_touch_pct,
    'last_touch_pct': last_touch_pct
}).fillna(0)
#round percentages for cleaner display
channel_stats = channel_stats.round(2)
#make index a column
channel_stats.reset_index(level=0, inplace=True)
#Average subtotal by first touch channel
avg_subtotal_first = joined_df.groupby('first_touch_channel')['SUBTOTAL'].mean().reset_index()
avg_subtotal_first.columns = ['first_touch_channel', 'avg_subtotal_first']
# Average subtotal by last touch channel
avg_subtotal_last = joined_df.groupby('last_touch_channel')['SUBTOTAL'].mean().reset_index()
avg_subtotal_last.columns = ['last_touch_channel', 'avg_subtotal_last']

def display_first_touchpoints_pie():
    #pie chart for first touch pct
    # Plotting the pie chart
    first_touch_sorted = channel_stats.sort_values(by ='first_touch_pct')
    #first_touch_sorted.set_index('index')['first_touch_pct']

    # Create pie chart
    
    fig, ax = plt.subplots(figsize = (8,8))
    ax.pie(first_touch_sorted['first_touch_pct'], labels=first_touch_sorted['index'], autopct='%1.1f%%',textprops={'fontsize': 20}, colors =  sns.color_palette(tjx_colors), startangle=90)
    ax.set_title('First Touch Percentage by Channel', fontsize=30, weight='bold')

    st.pyplot(fig, width = "stretch")

def display_last_touchpoints_pie():
    #pie chart for first touch pct
    # Plotting the pie chart
    last_touch_sorted = channel_stats.sort_values(by ='last_touch_pct')
    #Get rid of 0 percent
    last_touch_sorted = last_touch_sorted[last_touch_sorted['last_touch_pct'] != 0]
    # Create pie chart
    
    fig, ax = plt.subplots(figsize = (8,8))
    ax.pie(last_touch_sorted['last_touch_pct'], labels=last_touch_sorted['index'], autopct='%1.1f%%',textprops={'fontsize': 20}, colors = sns.color_palette(tjx_colors), startangle=90)
    ax.set_title('Last Touch Percentage by Channel', fontsize=30, weight='bold')

    st.pyplot(fig, width = "stretch")

def display_channel_sales_bar():
    # Count conversions per channel
    conversion_counts = touchpoints_df.groupby(['CHANNEL', 'CONVERTED_FLAG']).size().unstack(fill_value=0)

    # Plotting
    fig, ax = plt.subplots()
    conversion_counts.plot(kind='bar', ax=ax, color = ['#9C1C26', '#e56f78'])

    # Customize chart
    ax.set_title('Conversions by Channel')
    ax.set_xlabel('Channel')
    ax.set_ylabel('Count')
    ax.legend(title='Checkout')

    st.pyplot(fig, width = "stretch")

def display_avg_touchpoints_metric():
    id_counts = touchpoints_df['CUSTOMER_ID'].value_counts()
    average_occurrences = id_counts.mean()
    average_occurrences = round(average_occurrences, 2)
    max_occurences = id_counts.max()
    max_occurences = round(max_occurences,2)
    st.metric(label = "Average # of Touchpoints:  \n", value = average_occurrences, border = True)
    st.metric(label = "Maximum # of Touchpoints:  \n", value = max_occurences, border = True)


def display_last_touch_sales_bar():
    # Average subtotal by last touch channel
    avg_subtotal_last_sorted = avg_subtotal_last.sort_values(by='avg_subtotal_last',ascending=False)
    # Plotting
    fig, ax = plt.subplots()
    avg_subtotal_last_sorted.plot(x="last_touch_channel", y="avg_subtotal_last", kind="bar", color =  sns.color_palette(tjx_colors),legend=False, ax =ax)
    plt.title("Average Sale by Last Touchpoint Channel")
    plt.xlabel("Channel")
    plt.ylabel("Sales in USD ($)")
    st.pyplot(fig, width= 'stretch')

#OUTPUT ITEMS
st.markdown("<h1 style='text-align: center; color: #9C1C26;'>Customer Touchpoint Analysis</h1>", unsafe_allow_html=True)
row1 = st.columns(3, border= True)
r1c1 = row1[0]
r1c2 = row1[1]
r1c3 = row1[2]

row2 = st.columns(2, border = True)
r2c1 = row2[0]
r2c2 = row2[1]





with r1c1:
    display_first_touchpoints_pie()

with r1c2:
    display_last_touchpoints_pie()

with r1c3:
    display_avg_touchpoints_metric()

with r2c1:
    display_channel_sales_bar()

with r2c2:
    display_last_touch_sales_bar()
    


st.text("")
st.text("")
