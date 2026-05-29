import pandas as pd
import streamlit as st
import plotly.express as px

# Page config
st.set_page_config(page_title="Ferry Analytics", page_icon="🚢", layout="wide")

# Load data
df = pd.read_csv("data/Toronto Island Ferry Tickets (1).csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Feature Engineering
df['Hour'] = df['Timestamp'].dt.hour
df['Month'] = df['Timestamp'].dt.month
df['Year'] = df['Timestamp'].dt.year
df['Day_of_Week'] = df['Timestamp'].dt.day_name()
df['Is_Weekend'] = df['Timestamp'].dt.dayofweek >= 5
df['Season'] = df['Month'].map({
    12:'Winter',1:'Winter',2:'Winter',
    3:'Spring',4:'Spring',5:'Spring',
    6:'Summer',7:'Summer',8:'Summer',
    9:'Fall',10:'Fall',11:'Fall'
})
df['Total_Tickets'] = df['Redemption Count'] + df['Sales Count']

# Sidebar Filters
st.sidebar.title("🔍 Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
selected_season = st.sidebar.multiselect("Select Season", df['Season'].unique(), default=df['Season'].unique())

# Filter data
filtered = df[(df['Year'] == selected_year) & (df['Season'].isin(selected_season))]

# Title
st.title("🚢 Ferry Capacity Utilization Dashboard")
st.markdown(f"Showing data for **{selected_year}**")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", f"{filtered['Total_Tickets'].sum():,.0f}")
col2.metric("Avg Tickets per 15 min", f"{filtered['Total_Tickets'].mean():.1f}")
col3.metric("Peak Hour", f"{filtered.groupby('Hour')['Total_Tickets'].mean().idxmax()}:00")

st.divider()

# Chart 1 - Busiest Hours
st.subheader("⏰ Busiest Hours")
hour_data = filtered.groupby('Hour')['Total_Tickets'].mean().reset_index()
fig1 = px.bar(hour_data, x='Hour', y='Total_Tickets', color='Total_Tickets')
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Monthly Trend
st.subheader("📅 Monthly Trend")
month_data = filtered.groupby('Month')['Total_Tickets'].mean().reset_index()
fig2 = px.line(month_data, x='Month', y='Total_Tickets', markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Season Summary
st.subheader("🍂 Season Summary")
season_data = filtered.groupby('Season')['Total_Tickets'].mean().reset_index()
fig3 = px.pie(season_data, names='Season', values='Total_Tickets')
st.plotly_chart(fig3, use_container_width=True)

# Chart 4 - Weekday vs Weekend
st.subheader("📆 Weekday vs Weekend")
weekend_data = filtered.groupby('Is_Weekend')['Total_Tickets'].mean().reset_index()
weekend_data['Type'] = weekend_data['Is_Weekend'].map({True:'Weekend', False:'Weekday'})
fig4 = px.bar(weekend_data, x='Type', y='Total_Tickets', color='Type')
st.plotly_chart(fig4, use_container_width=True)
# Chart 5 - Yearly Trend
st.subheader("📈 Yearly Trend (2015-2025)")
yearly_data = df.groupby('Year')['Total_Tickets'].sum().reset_index()
fig5 = px.line(yearly_data, x='Year', y='Total_Tickets', markers=True, title="Total Tickets Per Year")
st.plotly_chart(fig5, use_container_width=True)