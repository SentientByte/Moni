import pandas as pd

def calculate_metrics(df):
    total_spent = abs(df[df.amount < 0]["amount"].sum())
    total_payments = abs(df[df.description.str.contains("PAYMENT RECEIVED THANK YOU", case=False)]["amount"].sum())
    return total_spent, total_payments

def get_category_table(df):
    return (
        df[df.amount < 0]
        .groupby("category_ai")["amount"]
        .sum()
        .abs()
        .reset_index()
        .rename(columns={"amount": "Total Spent"})
        .sort_values("Total Spent", ascending=False)
    )

def get_daily_table(df):
    return (
        df[df.amount < 0]
        .groupby("date")["amount"]
        .sum()
        .abs()
        .reset_index()
        .rename(columns={"amount": "Total Spent"})
    )
