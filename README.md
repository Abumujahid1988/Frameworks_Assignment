# CORD-19 Metadata Analysis (Zenodo Snapshot)

This project analyzes the CORD-19 metadata snapshot from **2020-03-13**, file name:
`all_sources_metadata_2020-03-13.csv` (~49.8 MB).

## Setup

1. Download the dataset from Zenodo:
   ```bash
   curl -L -o all_sources_metadata_2020-03-13.csv \\
     "https://zenodo.org/record/3715500/files/all_sources_metadata_2020-03-13.csv?download=1"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run analysis:
   ```bash
   python analysis_script.py
   ```
4. Run analysis via jupyter notebook:
   ```bash
   analysis_notebook.ipynb
   ```
5. Run Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Outputs

- Cleaned dataset: `metadata_cleaned.csv`
- Visualizations in `outputs/`:
  - `publications_by_year.png`
  - `top_journals.png`
  - `title_wordcloud.png`
