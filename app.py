import streamlit as st
import data_loader
import categorizer
import aggregator
import visualizer

st.title("Personal Finance Dashboard")

uploaded_file = st.file_uploader("Upload your CSV or PDF file", type=["csv", "pdf"])

if uploaded_file:
    df = data_loader.load_transactions(uploaded_file)
    st.write("Sample transactions:", df.head())

    df = categorizer.classify_transactions(df)
    st.write("Categorized transactions:", df.head())

    agg_df = aggregator.aggregate_by_month_category(df)
    st.write("Aggregated spending:", agg_df)

    st.subheader("Monthly Spending Chart")
    visualizer.plot_monthly_spending(agg_df)
