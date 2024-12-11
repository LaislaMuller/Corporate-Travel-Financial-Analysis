import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random

# Configuring the page for dark mode
st.set_page_config(page_title="Corporate Travel Financial Model", layout="wide")

# Generate fictional employee names
def generate_employee_name():
    names = ['John Silva', 'Ana Souza', 'Carlos Almeida', 'Maria Oliveira', 'Pedro Costa', 'Fernanda Lima', 'Luciana Rocha', 'Ricardo Pereira']
    return random.choice(names)

# Cost centers for the trips
cost_centers = [
    'Corporate Event A', 'Corporate Event B', 'Corporate Event C', 
    'Corporate Event D', 'Corporate Event E', 'Corporate Event F', 
    'Corporate Event G', 'Sales', 'Negotiation', 'Support'
]

# Generate flight values
def generate_flight_value(flight_type):
    if flight_type == "National":
        return round(random.uniform(300, 700), 2)  # National flights are cheaper
    else:
        return round(random.uniform(700, 1500), 2)  # International flights are more expensive

# Generate flight data
def generate_flight_data(n):
    flight_data = []
    for _ in range(n):
        employee_name = generate_employee_name()
        cost_center = random.choice(cost_centers)
        flight_type = random.choice(["National", "International"])
        flight_value = generate_flight_value(flight_type)
        within_policy = "Yes" if flight_value <= 700 else "No"
        flight_data.append([employee_name, cost_center, flight_type, flight_value, within_policy])
    return flight_data

# Generate the flight data
flight_data = generate_flight_data(1000)
df_flights = pd.DataFrame(flight_data, columns=["Employee Name", "Cost Center", "Flight Type", "Flight Value", "Within Policy"])

# Calculate the total spent
total_spent = df_flights["Flight Value"].sum()

# Project for the next year with 5% inflation
inflation = 0.05
projected_next_year = total_spent * (1 + inflation)

# Flights within and outside policy
flights_within = df_flights[df_flights["Within Policy"] == "Yes"]
flights_outside = df_flights[df_flights["Within Policy"] == "No"]

# Total spent within and outside policy
total_within = flights_within["Flight Value"].sum()
total_outside = flights_outside["Flight Value"].sum()

# Savings calculation
savings = total_outside - total_within
average_savings = savings / len(flights_outside) if len(flights_outside) > 0 else 0

# Distribution by cost center
distribution_within = flights_within.groupby("Cost Center")["Flight Value"].sum()
distribution_outside = flights_outside.groupby("Cost Center")["Flight Value"].sum()

# Dashboard

# Title of the dashboard
st.title("Corporate Travel Financial Analysis")

# Main information
st.subheader("Spending Summary")
st.write(f"**Current Total Spend:** R$ {total_spent:,.2f}")
st.write(f"**Projection for Next Year (with 5% Inflation):** R$ {projected_next_year:,.2f}")
st.write(f"**Average Savings per Flight Outside the Policy:** R$ {average_savings:,.2f}")

# Graph of total spending within and outside the policy
fig_spending = go.Figure()

fig_spending.add_trace(go.Bar(
    x=["Within Policy", "Outside Policy"],
    y=[total_within, total_outside],
    name="Spending",
    marker_color=['#2ca02c', '#d62728']
))

fig_spending.update_layout(
    title="Spending Within and Outside the Policy",
    xaxis_title="Category",
    yaxis_title="Value (R$)",
    template="plotly_dark"
)

st.plotly_chart(fig_spending, use_container_width=True)

# Graph of distribution by cost center
fig_distribution = go.Figure()

fig_distribution.add_trace(go.Bar(
    x=distribution_within.index,
    y=distribution_within.values,
    name="Within Policy",
    marker_color='#2ca02c'
))

fig_distribution.add_trace(go.Bar(
    x=distribution_outside.index,
    y=distribution_outside.values,
    name="Outside Policy",
    marker_color='#d62728'
))

fig_distribution.update_layout(
    title="Spending Distribution by Cost Center",
    xaxis_title="Cost Center",
    yaxis_title="Value (R$)",
    barmode='stack',
    template="plotly_dark"
)

st.plotly_chart(fig_distribution, use_container_width=True)

# Graph for the spending projection for the next year
fig_projection = go.Figure()

years = [2023, 2024]
values = [total_spent, projected_next_year]

fig_projection.add_trace(go.Scatter(
    x=years,
    y=values,
    mode='lines+markers',
    name="Spending Projection",
    line=dict(color='blue', width=4)
))

# Adding variation markers for a more formal appearance
fig_projection.add_trace(go.Scatter(
    x=years, 
    y=[total_spent * 1.05, projected_next_year * 1.05], 
    mode="lines+markers", 
    name="5% Increase", 
    line=dict(color="orange", dash="dash")
))

fig_projection.update_layout(
    title="Spending Projection for Next Year",
    xaxis_title="Year",
    yaxis_title="Value (R$)",
    template="plotly_dark"
)

st.plotly_chart(fig_projection, use_container_width=True)

# Insights on spending
st.subheader("Spending Insights")
st.write(f"Total spent within the policy: **R$ {total_within:,.2f}**")
st.write(f"Total spent outside the policy: **R$ {total_outside:,.2f}**")
st.write(f"Total savings comparing within and outside the policy: **R$ {savings:,.2f}**")
