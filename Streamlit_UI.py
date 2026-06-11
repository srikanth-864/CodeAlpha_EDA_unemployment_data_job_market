import os
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

st.title("📊Unemployment In India Dashboard \n \n")
st.write("Analysis of unemployment rate trends, COVID-19 impact, and regional patterns.")

option = st.sidebar.selectbox(
    "Select Analysis:",
    [
        "Average Unemployment rate by region",
        "Average Unemployment rate overtime",
        "Change in Average Unemployment Rate by Region",
        "Distribution of unemployment Rates in india",
        "Labour Participation vs Unemployment Rate",
        "UnEmployment Rate Before and During Covid"
    ]
)

if option == "Average Unemployment rate by region":
    st.image(
        os.path.join(IMAGE_DIR, "Average Unemployment rate by region.png"),
        use_container_width=True
    )

elif option == "Average Unemployment rate overtime":
    st.image(
        os.path.join(IMAGE_DIR, "Average Unemployment rate overtime.png"),
        use_container_width=True
    )

elif option == "Change in Average Unemployment Rate by Region":
    st.image(
        os.path.join(IMAGE_DIR, "Change in Average Unemployment Rate by Region.png"),
        use_container_width=True
    )

elif option == "Distribution of unemployment Rates in india":
    st.image(
        os.path.join(IMAGE_DIR, "Distribution of unemployment Rates in india.png"),
        use_container_width=True
    )

elif option == "Labour Participation vs Unemployment Rate":
    st.image(
        os.path.join(IMAGE_DIR, "Labour Participation vs Unemployment Rate.png"),
        use_container_width=True
    )

elif option == "UnEmployment Rate Before and During Covid":
    st.image(
        os.path.join(IMAGE_DIR, "UnEmployment Rate Before and During Covid.png"),
        use_container_width=True
    )

# Reading The File
csv_path = os.path.join(BASE_DIR, "Cleaned_Data.csv")
df = pd.read_csv(csv_path)

df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Regions:",
    df["Region"].unique(),
    default=df["Region"].unique()
)

areas = st.sidebar.multiselect(
    "Select Area:",
    df["Area"].unique(),
    default=df["Area"].unique()
)

filtered_df = df[
    df["Region"].isin(regions) &
    df["Area"].isin(areas)
]

# Main Dashboard
st.subheader("📅Overall Trend")

fig = px.line(
    filtered_df,
    x="Date",
    y="UnEmployment(%)",
    color="Region"
)

st.plotly_chart(fig, use_container_width=True)

# Covid Impact
st.subheader("Covid Impact on India Unemployment Rate")

covid_start = pd.Timestamp("2020-03-01")

pre_covid = filtered_df[filtered_df["Date"] < covid_start]
during_covid = filtered_df[filtered_df["Date"] >= covid_start]

pre_mean = pre_covid["UnEmployment(%)"].mean()
during_mean = during_covid["UnEmployment(%)"].mean()

col1, col2 = st.columns(2)

col1.metric(
    "Pre-COVID Avg Unemployment (%)",
    f"{pre_mean:.2f}"
)

col2.metric(
    "During-COVID Avg Unemployment (%)",
    f"{during_mean:.2f}"
)

region_change = (
    during_covid.groupby("Region")["UnEmployment(%)"].mean()
    - pre_covid.groupby("Region")["UnEmployment(%)"].mean()
).sort_values(ascending=False).dropna()

st.bar_chart(region_change)