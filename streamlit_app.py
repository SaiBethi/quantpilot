import streamlit as st

# Page config
st.set_page_config(page_title="QuantPilot - Home", layout="wide", page_icon="📈")

# Load custom font + CSS
def local_css():
    css = """
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap');

    html, body, [class*="css"]  {
        font-family: 'EB Garamond', serif;
        scroll-behavior: smooth;
        background-color: #f7f9fc;
        color: #222222;
    }

    /* Hero section background */
    .hero {
        background-image: url('https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        margin-bottom: 3rem;
    }

    .hero h1 {
        font-size: 4rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }

    .hero p {
        font-size: 1.5rem;
        margin-top: 1rem;
        max-width: 700px;
        text-align: center;
    }

    .btn-primary {
        margin-top: 2rem;
        background-color: #0072C6;
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.25rem;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .btn-primary:hover {
        background-color: #005a9e;
    }

    /* Section styling */
    .section {
        max-width: 900px;
        margin: auto;
        padding: 2rem 1rem;
        color: #333;
    }

    .section h2 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .section p {
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: center;
    }

    /* Footer */
    footer {
        margin-top: 4rem;
        padding: 1rem;
        text-align: center;
        color: #777;
        font-size: 0.9rem;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


local_css()

# Hero section
st.markdown(
    """
    <div class="hero">
        <h1>📈 QuantPilot</h1>
        <p>Your AI-powered stock dashboard and finance insights hub.</p>
        <button class="btn-primary" onclick="window.location.href='/pages/01_Dashboard'">Go to Dashboard →</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# About section
st.markdown(
    """
    <div class="section">
        <h2>Why QuantPilot?</h2>
        <p>
            QuantPilot empowers you with elegant data visualizations and AI insights for smarter stock market decisions.  
            Built with Streamlit, Plotly, and powered by cutting-edge AI models, QuantPilot makes finance accessible to everyone.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Features section
st.markdown(
    """
    <div class="section">
        <h2>Features</h2>
        <p>• Real-time stock charts with technical indicators like Moving Averages, RSI, and more.<br>
           • AI-driven predictions and sentiment analysis.<br>
           • Easy CSV data export.<br>
           • Clean, responsive, and beautiful interface designed with El Garamond font.<br>
           • And much more coming soon!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer
st.markdown(
    """
    <footer>
        © 2025 QuantPilot | Made with ❤️ by You
    </footer>
    """,
    unsafe_allow_html=True,
)