def aggregate_by_month_category(df):
    """
    Aggregate spending sums by month and category.
    Expects df to have columns: date, amount, category
    """
    df['month'] = df['date'].dt.to_period('M')
    agg = df.groupby(['month', 'category'])['amount'].sum().reset_index()
    agg['month'] = agg['month'].dt.to_timestamp()
    return agg
