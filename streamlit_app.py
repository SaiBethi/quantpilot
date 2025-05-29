import streamlit as st

st.set_page_config(page_title="QuantPilot", layout="wide", page_icon="📈")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/styles.css")

st.title("📈 QuantPilot: AI-Powered Stock Dashboard")
st.markdown(
    """
    Welcome to QuantPilot!  
    Use the sidebar to explore the Dashboard, AI Insights, and more.  
    Powered by Streamlit and Plotly, designed with El Garamond font for elegance.
    """
)

st.image(
    "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1350&q=80",
    caption="Your finance insights hub.",
    use_column_width=True,
)