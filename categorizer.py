from transformers import pipeline
import torch
import re

# Define target categories
candidate_labels = [
    "groceries", "utilities", "entertainment", "transport", "dining",
    "salary", "shopping", "payments", "automotive", "health", "government", "others"
]

# Use GPU if available
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device
)

# Keyword-based category map
CATEGORY_KEYWORDS = {
    "payments": ["payment received thank you"],
    "groceries": ["supermarket", "market", "mini mart", "aswaq", "lulu", "tawfeer", "ewa"],
    "transport": ["petrol", "station"],
    "dining": ["cafe", "bakery", "ceasers", "bateel", "restaurant"],
    "automotive": ["spare parts", "auto"],
    "shopping": ["fashion", "perfumes", "electronics", "sports", "house trading", "shoe", "r and b", "max"],
    "government": ["moi", "batelco"],
    "health": ["pharmacy"],
    "utilities": ["ewa", "batelco","MOI",'eGov'],
    "others": []
}

def keyword_category(description):
    """Check description against known keywords."""
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return category
    return None

def categorize(df):
    """Assign category to each transaction using keyword match or LLaMA fallback."""
    categories = []
    for desc in df["description"]:
        cat = keyword_category(desc)
        if not cat:
            result = classifier(desc, candidate_labels)
            cat = result["labels"][0] if result and "labels" in result else "others"
        categories.append(cat)
    df["category_ai"] = categories
    return df
