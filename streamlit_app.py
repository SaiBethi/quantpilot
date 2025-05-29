import streamlit as st
import streamlit.components.v1 as components

# Set custom font and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'EB Garamond', serif;
        scroll-behavior: smooth;
    }
    .hero {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
        url('https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2015&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        padding: 100px 30px;
        text-align: center;
    }
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        margin: 2rem 0 1rem;
    }
    .feature-card {
        background-color: white;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem 0;
        font-size: 0.9rem;
        color: #6B7280;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero">
        <h1 style="font-size: 4rem; font-weight: bold;">📈 QuantPilot</h1>
        <p style="font-size: 1.5rem; max-width: 700px; margin: 1rem auto;">
            AI-powered financial analytics for data-driven investment decisions
        </p>
        <a href="/dashboard" target="_self">
            <button style="padding: 0.75rem 2rem; font-weight: bold; background-color: white; color: #1f2937; border-radius: 8px; font-size: 1rem; margin-top: 1.5rem;">Launch Dashboard</button>
        </a>
    </div>
""", unsafe_allow_html=True)

# About Section
st.markdown("<h2 class='section-title'>About QuantPilot</h2>", unsafe_allow_html=True)
cols = st.columns(3)

about_data = [
    ("🔍", "Advanced Analytics", "QuantPilot leverages cutting-edge algorithms to analyze financial data with precision, uncovering hidden patterns and opportunities."),
    ("🤖", "AI-Powered", "Our machine learning models continuously learn from market data to provide increasingly accurate predictions and insights."),
    ("📊", "Visual Intelligence", "Complex financial data transformed into intuitive visualizations that tell the story behind the numbers.")
]

for i, col in enumerate(cols):
    with col:
        st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem;">{about_data[i][0]}</div>
                <div class="feature-title">{about_data[i][1]}</div>
                <p style="color: #4B5563">{about_data[i][2]}</p>
            </div>
        """, unsafe_allow_html=True)

# Features Section
st.markdown("<h2 class='section-title'>Key Features</h2>", unsafe_allow_html=True)
features = [
    ("📉", "Interactive Charts", "Explore your data with dynamic, zoomable charts that update in real-time as you adjust parameters."),
    ("🧠", "AI Predictions", "Get forward-looking insights with our proprietary AI models trained on decades of market data."),
    ("📈", "Technical Indicators", "Analyze market trends using popular indicators like RSI, MACD, and Bollinger Bands."),
    ("📋", "Stock Summary", "View essential metrics like PE ratio, market cap, and dividend yield at a glance."),
    ("📁", "Downloadable Reports", "Export your results and insights in CSV format for offline analysis or presentation.")
]

for i in range(0, len(features), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(features):
            with cols[j]:
                icon, title, desc = features[i + j]
                st.markdown(f"""
                    <div class="feature-card">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <p style="color: #4B5563">{desc}</p>
                    </div>
                """, unsafe_allow_html=True)

# Contact Section
st.markdown("<h2 class='section-title'>Contact</h2>", unsafe_allow_html=True)
st.markdown("""
    <div class="feature-card" style="text-align:center;">
        <p>Have questions or feedback?</p>
        <p>Email us at <a href="mailto:team@quantpilot.ai">team@quantpilot.ai</a></p>
        <p>Follow us on <a href="https://twitter.com/quantpilot" target="_blank">Twitter</a> and <a href="https://linkedin.com/company/quantpilot" target="_blank">LinkedIn</a></p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
""", unsafe_allow_html=True)