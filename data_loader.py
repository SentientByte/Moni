import pandas as pd
import io
from categorizer import parse_pdf_to_df

def load_transactions(uploaded_file) -> pd.DataFrame:
    """
    Load transactions from a CSV or PDF upload.
    For CSV: expects columns Date, Description, Amount.
    For PDF: extracts and parses into standard format.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        # Try reading with UTF-8 first, fallback if needed
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="latin1", errors="replace")

        df.columns = [col.strip().lower() for col in df.columns]

        expected_cols = {'date', 'description', 'amount'}
        if not expected_cols.issubset(df.columns):
            raise ValueError(f"CSV must contain columns: {expected_cols}")

        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['date', 'description', 'amount'])
        return df.reset_index(drop=True)

    elif filename.endswith(".pdf"):
        return parse_pdf_to_df(uploaded_file)

    else:
        raise ValueError("Unsupported file type. Please upload a CSV or PDF.")
