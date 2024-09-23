

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import re

# Title for the app
st.title("MSBA325 Assignment - Interactive Visualizations")



# Load your CSV dataset
data_url = 'https://linked.aub.edu.lb/pkgcube/data/09aeb9066db2534a24e89e862ec15106_20240908_154639.csv'
data = pd.read_csv(data_url)

# Regular expression pattern to extract the last part of the URL
pattern = r'https?://[a-zA-Z.]+/[a-zA-Z]+/([a-zA-Z_]+)'
data['District'] = data['refArea'].apply(lambda x: re.search(pattern, x).group(1) if re.search(pattern, x) else None)

# Education levels
education_levels = [
    'PercentageofEducationlevelofresidents-highereducation',
    'PercentageofEducationlevelofresidents-secondary',
    'PercentageofEducationlevelofresidents-intermediate',
    'PercentageofEducationlevelofresidents-vocational',
    'PercentageofEducationlevelofresidents-elementary',
    'PercentageofEducationlevelofresidents-university',
    'PercentageofEducationlevelofresidents-illeterate'
]

# Remove rows where all education level columns are NaN
data_cleaned = data.dropna(subset=education_levels, how='all')

# Streamlit app title
st.title('Education Levels in Lebanon')

# Dropdown for selecting district
district = st.selectbox("Select a District", data_cleaned['District'].unique())

# Pie Chart for the first town in the selected district
st.subheader(f"Education Levels in {district}")
district_data = data_cleaned[data_cleaned['District'] == district]
first_town = district_data['Town'].unique()[0]
town_data = district_data[district_data['Town'] == first_town]

# Pie Chart
fig_pie = px.pie(town_data, names=education_levels, 
                 values=[town_data[col].values[0] for col in education_levels], 
                 title=f'Education Levels in {first_town}, {district}')
st.plotly_chart(fig_pie)

# Stacked Bar Chart for all towns in the selected district
st.subheader(f"Stacked Bar Chart for Towns in {district}")
fig_bar = go.Figure()
for town in district_data['Town'].unique():
    town_data = district_data[district_data['Town'] == town]
    percentages = [town_data[col].values[0] for col in education_levels]
    fig_bar.add_trace(go.Bar(
        x=education_levels,
        y=percentages,
        name=town
    ))

fig_bar.update_layout(
    title=f'Stacked Education Levels by Town in {district}',
    xaxis_title='Education Level',
    yaxis_title='Percentage',
    barmode='stack',
    yaxis=dict(range=[0, 100]),
    plot_bgcolor='rgba(240, 240, 240, 0.8)',
    paper_bgcolor='white'
)
st.plotly_chart(fig_bar)

# Box Plot for Higher Education Comparison Across Districts
st.subheader("Higher Education Comparison Across Districts")
boxplot_data = data_cleaned[['District', 'PercentageofEducationlevelofresidents-highereducation']]
fig_box = px.box(
    boxplot_data,
    x='District',
    y='PercentageofEducationlevelofresidents-highereducation',
    title='Comparison of Higher Education Percentage Across Districts',
    labels={'PercentageofEducationlevelofresidents-highereducation': 'Percentage of Higher Education'},
    boxmode='group'
)
fig_box.update_layout(
    plot_bgcolor='rgba(240, 240, 240, 0.8)',
    paper_bgcolor='white',
    xaxis_title='District',
    yaxis_title='Percentage of Higher Education',
    yaxis=dict(range=[0, 100])
)
st.plotly_chart(fig_box)

# Line Chart for Exchange Rate Over Time (assuming you have another dataset for this)
st.subheader("Exchange Rate (L.L. per USD) Over Time")
exchange_rate_data_url = 'https://linked.aub.edu.lb/pkgcube/data/8d63feb2c7b50a7f34a46290b4d3cabb_20240907_121244.csv'
exchange_rate_data = pd.read_csv(exchange_rate_data_url)
line_chart = px.line(exchange_rate_data, x='Year', y='Value', 
                     title='Exchange Rate (Lebanese Lira per USD) Over Time', 
                     labels={'Value': 'L.L. per USD', 'Year': 'Year'})
st.plotly_chart(line_chart)

