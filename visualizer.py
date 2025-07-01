import plotly.express as px
import pandas as pd

def summary_stats(df):
    spent = df[df.amount < 0].amount.sum()
    income = df[df.amount > 0].amount.sum()
    num_days = (df["date"].max() - df["date"].min()).days + 1
    avg_daily = spent / num_days if num_days > 0 else 0
    return spent, income, avg_daily

def plot_category_bar(df):
    df_filtered = df[df["amount"] < 0]
    cat_totals = df_filtered.groupby("Category")["amount"].sum().abs().reset_index()
    fig = px.bar(
        cat_totals,
        x="amount",
        y="Category",
        orientation="h",
        color="Category",
        title="Spending by Category",
        labels={"amount": "Total Spent", "Category": "Category"},
        height=400
    )
    fig.update_layout(showlegend=False, margin=dict(t=40, b=30, l=30, r=30))
    return fig

def plot_daily_bar(df):
    daily = df[df.amount < 0].groupby("date")["amount"].sum().reset_index()
    fig = px.bar(
        daily,
        x="date",
        y="amount",
        title="Daily Spending Over Time",
        labels={"amount": "Total Spent"},
        height=400
    )
    fig.update_layout(margin=dict(t=40, b=30, l=30, r=30))
    return fig

def plot_pie(df):
    pie_data = df[df.amount < 0].groupby("Category")["amount"].sum().abs().reset_index()
    fig = px.pie(
        pie_data,
        names="Category",
        values="amount",
        title="Spending Distribution by Category",
        height=400
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(t=40, b=30, l=30, r=30))
    return fig
