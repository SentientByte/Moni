import streamlit as st
from data_loader import load_transactions
from categorizer import categorize
from logic import calculate_metrics, get_category_table, get_daily_table
from ui_components import (
    show_summary_metrics,
    show_category_section,
    show_daily_section,
    render_transactions_aggrid,
)

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

    # ---- Metrics and Tables ----
    total_spent, total_payments = calculate_metrics(df)
    show_summary_metrics(total_spent, total_payments)

    category_table = get_category_table(df)
    show_category_section(category_table)

    daily_table = get_daily_table(df)
    show_daily_section(daily_table)

    # --- Transactions Table Section at Bottom ---
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.subheader("📄 Sample Transactions")
    show_all = st.checkbox("Show All Transactions")

    # Render editable transactions table using AgGrid
    updated_df = render_transactions_aggrid(df, show_all=show_all)

    # Apply category edits
    df["category_ai"] = updated_df["category_ai"]
