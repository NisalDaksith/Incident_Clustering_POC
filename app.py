##########################################
# app.py
##########################################
import streamlit as st
import pandas as pd
from utils import (
    load_csv,
    # preprocess_short_description,
    find_similar_short_tags,
    # preprocess_unique_resolution_notes,
    render_pie_charts,
)
from cosmetics import (
    set_page_layout,
    inject_custom_css,
    display_title,
    display_subheader,
    display_info_message,
    display_error_message,
    create_black_label,
)

# Set page layout and inject custom CSS
set_page_layout()
inject_custom_css()

# App title
display_title("Clustered Incident Analysis")

# Default CSV path
default_csv_path = "./Data/Clustered.csv"

# Load the dataset with error handling
try:
    df = load_csv(default_csv_path)
    display_info_message("CSV file successfully loaded!")
except Exception as e:
    display_error_message(f"Failed to load CSV: {e}")

# Upload CSV functionality
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        display_info_message("CSV file successfully loaded!")
    except Exception as e:
        display_error_message(f"Failed to load CSV: {e}")

# Display the dataset
display_subheader("Incidents")
st.dataframe(
    df[[
        "Incident",
        "Short_Description",
        "Long_Description",
        "Resolution_Notes",
        "State",
        "Assigned_to",
        "Final_Cluster",
    ]],
    use_container_width=True,
)

# Check for necessary columns
if "Short_Tags" in df.columns and "Final_Cluster" in df.columns:
    # Find similar rows
    display_subheader("Find Similar Rows by Short Description")
    short_description = st.text_input("Enter a Short Description:")

    if short_description:
        similar_rows, similarity_scores = find_similar_short_tags(short_description, df)

        # Extract top 5 clusters based on similarity
        top_clusters = (
            similar_rows.groupby("Final_Cluster")
            .size()
            .sort_values(ascending=False)
            .head(5)
            .index.tolist()
        )

        # Display cluster labels
        st.markdown("### Similar Clusters")
        cluster_labels = "".join(
            create_black_label(cluster) for cluster in top_clusters
        )
        st.markdown(cluster_labels, unsafe_allow_html=True)

        # Add cluster sorting dropdown
        selected_cluster = st.selectbox(
            "Select a Cluster to Filter:",
            options=["All"] + top_clusters,
        )

        if selected_cluster != "All":
            similar_rows = similar_rows[similar_rows["Final_Cluster"] == selected_cluster]

        # Display similar rows only if the cluster is selected
        if not similar_rows.empty:
            st.dataframe(
                similar_rows[
                    [
                        "Incident",
                        "Short_Description",
                        "Long_Description",
                        "Resolution_Notes",
                        "State",
                        "Assigned_to",
                        "Final_Cluster",
                    ]
                ],
                use_container_width=True,
            )

        # Render plots below similar dataframe
        display_subheader("Clustered Data Visualizations")
        columns_to_plot = ["State", "Assigned_to"]  # Example columns
        render_pie_charts(similar_rows, columns_to_plot)
else:
    display_error_message("Required columns ('Short_Tags' and 'Final_Cluster') are missing from the dataset.")