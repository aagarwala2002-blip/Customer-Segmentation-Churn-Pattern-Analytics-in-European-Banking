import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Bank Churn Analytics", page_icon="📊", layout="wide")
st.title("📊 Customer Segmentation & Churn Analytics")
st.markdown("Analyze European banking churn patterns across geographic, demographic, and financial segments.")
st.divider()

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("European_Bank_Segmented.csv")

df = load_data()

# 3. Sidebar: Dynamic Segment Filters
st.sidebar.header("🔍 Segment Filters")
st.sidebar.markdown("Filter the dashboard to drill down into specific customer bases.")
selected_geo = st.sidebar.multiselect("Geography", df['Geography'].unique(), default=df['Geography'].unique())
selected_age = st.sidebar.multiselect("Age Group", df['Age_Group'].dropna().unique(), default=df['Age_Group'].dropna().unique())
selected_gender = st.sidebar.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())

# Apply Filters
filtered_df = df[(df['Geography'].isin(selected_geo)) & 
                 (df['Age_Group'].isin(selected_age)) & 
                 (df['Gender'].isin(selected_gender))]

# 4. Dynamic KPIs (Key Performance Indicators)
st.header("1. Core Key Performance Indicators (KPIs)")
total_customers = len(filtered_df)
overall_churn = (filtered_df['Exited'].mean()) * 100

high_value_df = filtered_df[filtered_df['Balance_Segment'] == 'High-balance']
high_value_churn = (high_value_df['Exited'].mean()) * 100 if len(high_value_df) > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers in Segment", f"{total_customers:,}")
col2.metric("Overall Churn Rate", f"{overall_churn:.2f}%")
col3.metric("High-Value Churn Ratio", f"{high_value_churn:.2f}%")

st.info("💡 **Metric Insight:** The *High-Value Churn Ratio* tracks the exit rate of customers with balances exceeding €50,000. These accounts represent the highest immediate revenue risk to the institution.")

st.divider()

# 5. Visual Insights: Geography & Age
st.header("2. Geographic & Demographic Distribution")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Geographic Risk Index")
    geo_churn = filtered_df.groupby('Geography')['Exited'].mean().reset_index()
    geo_churn['Exited'] = geo_churn['Exited'] * 100
    fig_geo = px.bar(geo_churn, x='Geography', y='Exited', text_auto='.2f', 
                     title="Percentage of Churn by Country", 
                     labels={'Exited': 'Churn Rate (%)'}, color='Geography')
    st.plotly_chart(fig_geo, use_container_width=True)
    st.caption("📌 **What this means:** Highlights regional churn exposure. A higher bar indicates a geographic area requiring urgent localized retention strategies.")

with col_b:
    st.subheader("Age Segment Analysis")
    age_churn = filtered_df.groupby('Age_Group')['Exited'].mean().reset_index()
    age_churn['Exited'] = age_churn['Exited'] * 100
    fig_age = px.bar(age_churn, x='Age_Group', y='Exited', text_auto='.2f', 
                     title="Percentage of Churn by Age Bracket", 
                     labels={'Exited': 'Churn Rate (%)'}, color='Age_Group')
    st.plotly_chart(fig_age, use_container_width=True)
    st.caption("📌 **What this means:** Identifies generational churn trends. A spike in a specific age bracket suggests a misalignment between current bank products and that group's life-stage needs.")

st.divider()

# 6. High-Value Customer Explorer
st.header("3. High-Value Customer Explorer")
fig_scatter = px.scatter(filtered_df, x='EstimatedSalary', y='Balance', color='Exited', 
                         opacity=0.5, title="Salary vs. Balance Drill-Down (0 = Retained, 1 = Churned)",
                         labels={'Exited': 'Churn Status'},
                         color_continuous_scale=['#2ecc71', '#e74c3c'])
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption("📌 **What this means:** This scatter plot maps every filtered customer's wealth profile. Look for dense clusters of red (1) to instantly identify if high-salary or high-balance individuals are exiting the bank at alarming rates.")