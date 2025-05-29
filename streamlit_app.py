import streamlit as st
import time

# Page config
st.set_page_config(page_title="QuantPilot - Home", layout="wide", page_icon="📈")

# Custom CSS for font, layout, animations
def local_css():
    css = """
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap');

    html, body, [class*="css"] {
        font-family: 'EB Garamond', serif !important;
        scroll-behavior: smooth;
        background-color: #f0f4f8;
        color: #222222;
        margin: 0;
        padding: 0;
    }

    /* Sticky Navbar */
    nav {
        position: sticky;
        top: 0;
        background: #ffffffdd;
        backdrop-filter: saturate(180%) blur(10px);
        border-bottom: 1px solid #ddd;
        z-index: 9999;
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
    }
    nav a {
        color: #0072C6;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    nav a:hover {
        color: #004a7c;
        cursor: pointer;
    }

    /* Hero section */
    .hero {
        background-image: url('https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center center;
        height: 85vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        padding: 0 1rem;
        text-align: center;
    }
    .hero h1 {
        font-size: 5rem;
        margin-bottom: 0.2rem;
    }
    .hero p {
        font-size: 1.8rem;
        max-width: 720px;
        margin: 0 auto 2rem;
    }
    .btn-primary {
        background-color: #0072C6;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.4rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,114,198,0.4);
        user-select: none;
    }
    .btn-primary:hover {
        background-color: #004a7c;
    }

    /* Sections */
    section {
        max-width: 900px;
        margin: 5rem auto;
        padding: 2rem 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        opacity: 0;
        transform: translateY(30px);
        animation: fadeInUp 1s forwards;
    }

    /* Animation delay for multiple sections */
    section:nth-of-type(1) {
        animation-delay: 0.2s;
    }
    section:nth-of-type(2) {
        animation-delay: 0.5s;
    }
    section:nth-of-type(3) {
        animation-delay: 0.8s;
    }

    section h2 {
        font-size: 2.8rem;
        margin-bottom: 1rem;
        color: #0072C6;
        text-align: center;
    }
    section p {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #444;
        text-align: center;
    }

    /* Footer */
    footer {
        text-align: center;
        padding: 2rem 1rem;
        font-size: 1rem;
        color: #888;
    }

    /* Fade in up animation */
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

local_css()

# Sticky Navbar
st.markdown(
    """
    <nav>
        <a href="#hero">Home</a>
        <a href="#about">About</a>
        <a href="#features">Features</a>
        <a href="#contact">Contact</a>
    </nav>
    """,
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
    <section id="hero" class="hero">
        <h1>📈 QuantPilot</h1>
        <p>Your AI-powered stock dashboard and finance insights hub.</p>
        <button class="btn-primary" onclick="window.location.href='/pages/01_Dashboard'">Explore Dashboard →</button>
    </section>
    """,
    unsafe_allow_html=True,
)

# About Section
st.markdown(
    """
    <section id="about">
        <h2>Why QuantPilot?</h2>
        <p>
            QuantPilot empowers you with elegant data visualizations and AI insights for smarter stock market decisions.<br>
            Built with Streamlit, Plotly, and powered by cutting-edge AI models, QuantPilot makes finance accessible to everyone.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

# Features Section
st.markdown(
    """
    <section id="features">
        <h2>Features</h2>
        <p>
            • Real-time interactive stock charts with technical indicators like Moving Averages, RSI, Bollinger Bands, and more.<br>
            • AI-driven predictions and sentiment analysis.<br>
            • Easy CSV data export.<br>
            • Clean, responsive, and beautiful interface designed with El Garamond font.<br>
            • Future features coming soon!
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

# Contact Section
st.markdown(
    """
    <section id="contact">
        <h2>Get in Touch</h2>
        <p>
            Have questions or want to contribute? Reach out to us at <a href="mailto:contact@quantpilot.com">contact@quantpilot.com</a>
        </p>
    </section>
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