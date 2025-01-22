##########################################
# utils.py
##########################################
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

def load_csv(file_path):
    """Load CSV file and return DataFrame."""
    return pd.read_csv(file_path)

def preprocess_short_description(short_desc):
    """Preprocess short description to extract tags, handle errors, and clean unwanted characters."""
    if isinstance(short_desc, str):
        tags = re.findall(r'\b\w+\b', short_desc)
        cleaned_tags = []
        for tag in tags:
            if tag.isdigit():
                continue
            elif re.match(r'^[A-Za-z]+(\d+)[A-Za-z]*$', tag):
                cleaned_tags.append(re.sub(r'\d+', 'XXXXX', tag))
            elif re.match(r'^[A-Za-z]+\d+[A-Za-z]*$', tag):
                cleaned_tags.append(re.sub(r'\d+', 'XXXXX', tag))
            else:
                cleaned_tags.append(tag)
        return [tag.lower() for tag in cleaned_tags]
    else:
        return []

def find_similar_short_tags(input_desc, dataframe):
    """Find similar short tags from the input description."""
    input_tags = preprocess_short_description(input_desc)
    if not input_tags:
        return pd.DataFrame(), []

    input_tags_str = ' '.join(input_tags)
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), lowercase=False)
    tags_list = dataframe['Short_Tags'].apply(lambda x: ' '.join(eval(x)) if isinstance(x, str) else '')
    X = vectorizer.fit_transform(tags_list)
    input_vec = vectorizer.transform([input_tags_str])
    similarities = cosine_similarity(input_vec, X).flatten()
    similar_indices = similarities.argsort()[-20:][::-1]
    similar_rows = dataframe.iloc[similar_indices]

    return similar_rows, similarities[similar_indices]

def preprocess_unique_resolution_notes(resolution_notes):
    """Identify and extract unique resolution notes."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer()
    note_vectors = vectorizer.fit_transform(resolution_notes.fillna("").astype(str))
    unique_notes = []
    for idx, note in enumerate(resolution_notes):
        if not any(
                cosine_similarity(note_vectors[idx], note_vectors[other_idx])[0][0] > 0.9
                for other_idx in range(len(resolution_notes)) if idx != other_idx
        ):
            unique_notes.append(note)
    return unique_notes

def render_pie_charts(dataframe, columns):
    """Render pie charts for the given columns in the dataframe."""
    import matplotlib.pyplot as plt
    from streamlit.components.v1 import html

    cols = st.columns(2)  # Create two columns for side-by-side plots

    for idx, col in enumerate(columns):
        if col in dataframe.columns:
            values = dataframe[col].value_counts()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(values, labels=values.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"{col} Distribution")
            with cols[idx]:  # Render plot in the corresponding column
                st.pyplot(fig)