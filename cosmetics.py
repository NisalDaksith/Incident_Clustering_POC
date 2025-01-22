#########################################
# cosmetics.py
#########################################
import streamlit as st

def set_page_layout():
    """Set the Streamlit page layout to wide mode."""
    st.set_page_config(layout="wide")

def display_title(title):
    """Display the main title of the app."""
    st.title(title)

def display_subheader(subheader):
    """Display a subheader text."""
    st.subheader(subheader)

def display_info_message(message):
    """Display an informational message."""
    st.info(message)

def display_error_message(message):
    """Display an error message."""
    st.error(message)

def inject_custom_css():
    """Inject custom CSS styles for enhanced appearance."""
    custom_css = """
    <style>
        .stButton>button {
            border-radius: 5px;
            padding: 10px;
            margin: 2px;
            display: inline-block;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def create_black_label(cluster):
    """Create an HTML label for a cluster in black."""
    return f'<span style="display: inline-block; margin: 5px; padding: 10px; background-color: black; color: white; border-radius: 5px;">{cluster}</span>'
