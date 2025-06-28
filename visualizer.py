import plotly.express as px
import pandas as pd

def summary_stats(df):
    spent = df[df.amount < 0].amount.sum()
    income = df[df.amount > 0].amount.sum()
    return spent, income

def plot_category_bar(df):
    df_filtered = df[df["amount"] < 0]
    cat_totals = df_filtered.groupby("category_ai")["amount"].sum().abs().reset_index()
    fig = px.bar(
        cat_totals,
        x="amount",
        y="category_ai",
        orientation="h",
        color="category_ai",
        title="Spending by Category",
        labels={"amount": "Total Spent", "category_ai": "Category"},
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
    pie_data = df[df.amount < 0].groupby("category_ai")["amount"].sum().abs().reset_index()
    fig = px.pie(
        pie_data,
        names="category_ai",
        values="amount",
        title="Spending Distribution by Category",
        height=400
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(t=40, b=30, l=30, r=30))
    return fig
