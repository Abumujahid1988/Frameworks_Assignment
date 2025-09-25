import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("CORD-19 Metadata Explorer (Zenodo Snapshot)")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("all_sources_metadata_2020-03-13.csv")

df = load_data()

st.write("### Preview of Dataset", df.head())

# Data cleaning
threshold = 0.8 * len(df)
df_clean = df.dropna(axis=1, thresh=threshold)

# Detect publish time column
date_candidates = ["publish_time", "publish_date", "date"]
date_col = next((c for c in date_candidates if c in df_clean.columns), None)

if date_col:
    df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce")
    df_clean["year"] = df_clean[date_col].dt.year
else:
    df_clean["year"] = None

# Abstract word count
if "abstract" in df_clean.columns:
    df_clean["abstract_word_count"] = df_clean["abstract"].fillna("").apply(lambda x: len(x.split()))

# Sidebar year filter
if "year" in df_clean.columns and df_clean["year"].notna().any():
    year_filter = st.sidebar.slider("Select Year",
                                    int(df_clean["year"].min()),
                                    int(df_clean["year"].max()),
                                    int(df_clean["year"].min()))
    filtered_df = df_clean[df_clean["year"] == year_filter]
else:
    filtered_df = df_clean

st.write(f"### Filtered Data ({len(filtered_df)} rows)", filtered_df.head())

# Publications over time
if "year" in df_clean.columns and df_clean["year"].notna().any():
    st.subheader("Publications Over Time")
    fig, ax = plt.subplots()
    df_clean["year"].value_counts().sort_index().plot(kind="line", marker="o", ax=ax)
    st.pyplot(fig)

# Top journals
journal_candidates = ["journal", "journal_name", "publication", "source"]
journal_col = next((c for c in journal_candidates if c in df_clean.columns), None)

if journal_col:
    st.subheader("Top Journals")
    fig, ax = plt.subplots()
    top_journals = df_clean[journal_col].value_counts().head(10)
    sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax)
    st.pyplot(fig)

# Word cloud
if "title" in df_clean.columns:
    st.subheader("Word Cloud of Titles")
    titles = " ".join(df_clean["title"].dropna().astype(str).tolist())
    if titles.strip():
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

# Sources distribution
source_candidates = ["source_x", "source", "metadata_source"]
source_col = next((c for c in source_candidates if c in df_clean.columns), None)

if source_col:
    st.subheader("Top Metadata Sources")
    fig, ax = plt.subplots()
    source_counts = df_clean[source_col].value_counts().head(10)
    sns.barplot(y=source_counts.index, x=source_counts.values, ax=ax)
    st.pyplot(fig)
