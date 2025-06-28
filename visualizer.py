import matplotlib.pyplot as plt
import seaborn as sns

def plot_monthly_spending(agg_df):
    """
    Plot a line chart showing monthly spending per category.
    """
    plt.figure(figsize=(12,6))
    sns.lineplot(data=agg_df, x='month', y='amount', hue='category', marker='o')
    plt.title("Monthly Spending by Category")
    plt.ylabel("Amount")
    plt.xlabel("Month")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()
