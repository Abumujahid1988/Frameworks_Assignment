import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# Load dataset
df = pd.read_csv("all_sources_metadata_2020-03-13.csv")
print("Shape of dataset:", df.shape)

# Drop columns with >80% missing values
threshold = 0.8 * len(df)
df_clean = df.dropna(axis=1, thresh=threshold)

# -------------------------------
# Detect publish time column
# -------------------------------
date_candidates = ["publish_time", "publish_date", "date"]
date_col = next((c for c in date_candidates if c in df_clean.columns), None)

if date_col:
    df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce")
    df_clean["year"] = df_clean[date_col].dt.year
else:
    print("⚠️ No publish date column found; skipping year analysis.")
    df_clean["year"] = None

# Abstract word count
if "abstract" in df_clean.columns:
    df_clean["abstract_word_count"] = (
        df_clean["abstract"].fillna("").apply(lambda x: len(x.split()))
    )

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# Publications over time
# -------------------------------
if "year" in df_clean.columns and df_clean["year"].notna().any():
    papers_per_year = df_clean["year"].value_counts().sort_index()
    papers_per_year.plot(kind="line", marker="o", figsize=(10, 6),
                         title="Number of Publications Over Time")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.savefig("outputs/publications_over_time.png")
    plt.show()

# -------------------------------
# Top journals
# -------------------------------
journal_candidates = ["journal", "journal_name", "publication", "source"]
journal_col = next((c for c in journal_candidates if c in df_clean.columns), None)

if journal_col:
    top_journals = df_clean[journal_col].value_counts().head(10)
    sns.barplot(y=top_journals.index, x=top_journals.values)
    plt.title("Top 10 Journals by Publication Count")
    plt.xlabel("Count")
    plt.ylabel("Journal")
    plt.savefig("outputs/top_journals.png")
    plt.show()
else:
    print("⚠️ No journal column found; skipping top journals analysis.")

# -------------------------------
# Word cloud of titles
# -------------------------------
if "title" in df_clean.columns:
    titles = " ".join(df_clean["title"].dropna().astype(str).tolist())
    if titles.strip():
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("outputs/title_wordcloud.png")
        plt.show()

# -------------------------------
# Sources distribution
# -------------------------------
source_candidates = ["source_x", "source", "metadata_source"]
source_col = next((c for c in source_candidates if c in df_clean.columns), None)

if source_col:
    source_counts = df_clean[source_col].value_counts().head(10)
    sns.barplot(y=source_counts.index, x=source_counts.values)
    plt.title("Top Metadata Sources")
    plt.xlabel("Count")
    plt.ylabel("Source")
    plt.savefig("outputs/top_sources.png")
    plt.show()
else:
    print("⚠️ No source column found; skipping sources analysis.")

# Save cleaned data
df_clean.to_csv("outputs/metadata_cleaned.csv", index=False)
print("✅ Cleaned dataset saved to outputs/metadata_cleaned.csv")
