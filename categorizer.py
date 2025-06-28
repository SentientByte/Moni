import pandas as pd
import fitz  # PyMuPDF
from transformers import pipeline
import torch

# Setup LLaMA (or compatible) text classification model
candidate_labels = [
    "groceries", "utilities", "entertainment", "transport", "dining", "salary", "others"
]

device = 0 if torch.cuda.is_available() else -1
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

def parse_pdf_to_df(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    lines = [line.strip() for line in text.split("\n")]
    transactions = []
    i = 0

    print("--- DEBUG: Total lines extracted:", len(lines))

    while i < len(lines) - 4:
        try:
            posting_date = lines[i].strip()
            transaction_date = lines[i + 1].strip()
            description = lines[i + 2].strip()
            maybe_blank = lines[i + 3].strip()
            amount_line = lines[i + 4].strip()

            # Look for lines like "10.000 CR" or "12.500 DR"
            if not ("CR" in amount_line or "DR" in amount_line):
                i += 1
                continue

            parts = amount_line.split()
            if len(parts) < 2:
                i += 1
                continue

            amount_str = parts[0].replace(",", "")
            direction = parts[1].upper()
            amount = float(amount_str)
            if direction == "DR":
                amount = -amount

            # Use LLaMA (or equivalent model) to classify category
            cat_result = classifier(description, candidate_labels)
            category = cat_result["labels"][0] if cat_result and "labels" in cat_result else "others"

            transactions.append({
                "date": posting_date,
                "description": description,
                "amount": amount,
                "category": category
            })
            i += 5
        except Exception as e:
            print(f"Skipping block at line {i} due to error: {e}")
            i += 1

    print("Matched transactions:", len(transactions))

    df = pd.DataFrame(transactions)
    if df.empty:
        print("⚠️ No transactions parsed from PDF.")

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y", errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.dropna(subset=["date", "description", "amount"], inplace=True)
    return df.reset_index(drop=True)