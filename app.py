import streamlit as st
import pandas as pd
from data_loader import load_transactions
from categorizer import categorize

st.set_page_config(page_title="Moni: Smart Transaction Analyzer", layout="wide")

st.title("💸 Moni: Smart Transaction Analyzer")

uploaded_file = st.file_uploader("Upload your CSV or PDF file", type=["csv", "pdf"])

if uploaded_file:
    try:
        df = load_transactions(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
        st.stop()

    df = categorize(df)

    # Top summary metrics
    total_spent = df[df.amount < 0]["amount"].sum()
    total_payments = df[df.description.str.contains("PAYMENT RECEIVED THANK YOU", case=False)]["amount"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## 💰 Total Spending")
        st.markdown(f"### **{total_spent:.2f}**")
    with col2:
        st.markdown("## 💳 Payments Received")
        st.markdown(f"### **{total_payments:.2f}**")

    st.subheader("📄 Sample Transactions")
    st.dataframe(df.head(4), use_container_width=True)

    if st.button("Show All Transactions"):
        st.dataframe(df, use_container_width=True)

    st.subheader("🧾 Spending by Category")
    category_table = (
        df[df.amount < 0]
        .groupby("category_ai")["amount"]
        .sum()
        .abs()
        .reset_index()
        .rename(columns={"amount": "Total Spent"})
        .sort_values("Total Spent", ascending=False)
    )
    st.dataframe(category_table, use_container_width=True)

    st.subheader("📆 Daily Spending")
    daily_table = (
        df[df.amount < 0]
        .groupby("date")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "Total Spent"})
    )
    st.dataframe(daily_table, use_container_width=True)
