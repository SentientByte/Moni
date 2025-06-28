import pandas as pd
import io
import fitz  # PyMuPDF

def parse_pdf_to_df(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    lines = [line.strip() for line in text.split("\n")]
    transactions = []
    i = 0

    while i < len(lines) - 4:
        try:
            posting_date = lines[i].strip()
            transaction_date = lines[i + 1].strip()
            description = lines[i + 2].strip()
            maybe_blank = lines[i + 3].strip()
            amount_line = lines[i + 4].strip()

            if not ("CR" in amount_line or "DR" in amount_line):
                i += 1
                continue

            parts = amount_line.split()
            if len(parts) < 2:
                i += 1
                continue

            amount = float(parts[0].replace(",", ""))
            if parts[1].upper() == "DR":
                amount = -amount

            transactions.append({
                "date": posting_date,
                "description": description,
                "amount": amount
            })
            i += 5
        except Exception:
            i += 1

    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y", errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.dropna(subset=["date", "description", "amount"], inplace=True)
    return df.reset_index(drop=True)

def load_transactions(file):
    filename = file.name.lower()
    if filename.endswith(".csv"):
        df = pd.read_csv(file)
        df.columns = [col.strip().lower() for col in df.columns]
        if not {"date", "description", "amount"}.issubset(df.columns):
            raise ValueError("CSV must contain: date, description, amount")
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        return df.dropna(subset=["date", "description", "amount"]).reset_index(drop=True)
    elif filename.endswith(".pdf"):
        return parse_pdf_to_df(file)
    else:
        raise ValueError("Unsupported file type")
