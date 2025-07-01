import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

def show_summary_metrics(total_spent, total_payments):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## 💰 Total Spending")
        st.markdown(f"### **{total_spent:,.2f} BHD**")
    with col2:
        st.markdown("## 💳 Payments Received")
        st.markdown(f"### **{total_payments:,.2f} BHD**")

def show_category_section(category_table):
    st.subheader("🧾 Spending by Category")
    col1, col2 = st.columns([2, 2])
    with col1:
        st.dataframe(category_table, use_container_width=True)
    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=category_table['category_ai'],
            values=category_table['Total Spent'],
            hole=0.4,
            textinfo='label+percent',
            hoverinfo='label+value',
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(color='#000000', width=1)
            )
        )])
        fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

def show_daily_section(daily_table):
    st.subheader("📆 Daily Spending")
    st.dataframe(daily_table, use_container_width=True)

def show_transaction_table(df):
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.subheader("📄 Sample Transactions")

    show_all = st.checkbox("Show All Transactions")
    sample_data = df.copy()
    if not show_all:
        sample_data = sample_data.head(4)

    sample_data["Edit"] = "✏️"
    categories = sorted(df["category_ai"].unique())

    for i, row in sample_data.iterrows():
        cols = st.columns([2, 5, 2, 2, 1])
        cols[0].write(row["date"].strftime("%Y-%m-%d"))
        cols[1].write(row["description"])
        cols[2].write(f"{abs(row['amount']):,.2f} BHD")
        if f"edit_{i}" in st.session_state and st.session_state[f"edit_{i}"]:
            new_val = cols[3].selectbox("Category", categories, key=f"select_{i}", index=categories.index(row["category_ai"]))
            if new_val != row["category_ai"]:
                df.at[i, "category_ai"] = new_val
            if cols[4].button("✅", key=f"confirm_{i}"):
                st.session_state[f"edit_{i}"] = False
        else:
            cols[3].write(row["category_ai"])
            if cols[4].button("✏️", key=f"edit_btn_{i}"):
                st.session_state[f"edit_{i}"] = True

def render_transactions_aggrid(df: pd.DataFrame, show_all: bool = False) -> pd.DataFrame:
    display_df = df.copy()
    if not show_all:
        display_df = display_df.head(4)

    # Format amount column with currency and remove negative sign
    display_df["amount"] = display_df["amount"].abs()
    display_df["amount"] = display_df["amount"].map(lambda x: f"{x:,.2f} BHD")

    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_column("date", header_name="Date", type=["customDateTimeFormat"], custom_format_string="yyyy-MM-dd")
    gb.configure_column("description", header_name="Description", wrapText=True, autoHeight=True)
    gb.configure_column("amount", header_name="Amount", type=["numericColumn"], cellStyle={"textAlign": "right"})
    gb.configure_column(
        "category_ai",
        header_name="Category",
        editable=True,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": sorted(df["category_ai"].unique())},
    )

    # Minimal grid options to reduce chrome and hover effects
    gb.configure_grid_options(
        suppressRowHoverHighlight=True,
        suppressMovableColumns=True,
        suppressCellSelection=False,
        suppressFieldDotNotation=True,
        suppressMenuHide=True,
        suppressColumnVirtualisation=True,
        suppressHorizontalScroll=True,
    )

    grid_options = gb.build()
    grid_options["domLayout"] = "normal"
    grid_options["rowHeight"] = 30  # Match typical Streamlit row height

    grid_response = AgGrid(
        display_df,
        gridOptions=grid_options,
        theme="streamlit",
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        height=300 if not show_all else 600,
        reload_data=False,
    )

    return grid_response["data"] if grid_response["data"] is not None else display_df
