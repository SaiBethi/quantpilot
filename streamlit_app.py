import streamlit as st

# Global style for full-page background and Garamond font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'EB Garamond', serif !important;
        scroll-behavior: smooth;
        height: 100%;
        min-height: 100vh;
        background: 
            linear-gradient(rgba(25, 28, 36, 0.61), rgba(25, 28, 36, 0.67)),
            url('https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2015&q=80') no-repeat center center fixed;
        background-size: cover !important;
        background-attachment: fixed !important;
    }
    .main, .stApp {
        background: transparent !important;
    }
    .hero {
        color: white;
        padding: 7vw 5vw 5vw 5vw;
        text-align: center;
        background: rgba(0,0,0,0.00);
        box-shadow: none;
    }
    @media (max-width: 768px) {
        .hero {
            padding: 19vw 4vw 10vw 4vw;
        }
        .section-title {
            font-size: 2rem !important;
        }
    }
    .section-title {
        text-align: center;
        font-size: 2.3rem;
        margin: 2.5rem 0 1.5rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        color: #fff;
        text-shadow: 0 2px 12px rgba(0,0,0,0.28);
    }
    .feature-card {
        background: rgba(255,255,255,0.88);
        padding: 2rem 1.4rem;
        margin-bottom: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 24px -6px rgba(31, 41, 55, 0.13), 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.22s cubic-bezier(.18,.89,.32,1.28), box-shadow 0.22s;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        z-index: 1;
        font-family: 'EB Garamond', serif !important;
    }
    .feature-card:hover {
        transform: translateY(-7px) scale(1.04);
        box-shadow: 0 16px 32px -8px rgba(31,41,55,0.19), 0 4px 12px rgba(0,0,0,0.09);
        background: linear-gradient(105deg, #f7f4ee 60%, #ece6df 100%);
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
        color: #1c1d1f;
        font-family: 'EB Garamond', serif !important;
    }
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem 0;
        font-size: 0.98rem;
        color: #e3e3e3;
        background: rgba(25, 28, 36, 0.55);
        border-top: 1px solid #ececec25;
        font-family: 'EB Garamond', serif !important;
    }
    .dash-btn {
        padding: 0.85rem 2.3rem;
        font-weight: 600;
        background: #fff;
        color: #23272a;
        border-radius: 10px;
        font-size: 1.18rem;
        margin-top: 2rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        transition: background 0.16s, color 0.16s, box-shadow 0.18s;
        font-family: 'EB Garamond', serif !important;
    }
    .dash-btn:hover {
        background: #ebe5dc;
        color: #111;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    /* Responsive columns for features */
    @media (max-width: 900px) {
        .feature-card { font-size: 0.98rem; }
    }
    @media (max-width: 600px) {
        .feature-card { font-size: 0.93rem; padding: 1.3rem 0.7rem; }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero">
        <h1 style="font-size: min(10vw, 4.5rem); font-weight: bold; margin-bottom: 0.6em; text-shadow: 0 2px 14px rgba(0,0,0,0.35);">📈 QuantPilot</h1>
        <p style="font-size: min(4vw, 1.55rem); max-width: 720px; margin: 1.2rem auto 0.5em; text-shadow: 0 2px 12px rgba(0,0,0,0.32);">
            AI-powered financial analytics for data-driven investment decisions
        </p>
        <a href="/dashboard" target="_self" style="text-decoration: none;">
            <button class="dash-btn">Launch Dashboard</button>
        </a>
    </div>
""", unsafe_allow_html=True)

# About Section
st.markdown("<h2 class='section-title'>About QuantPilot</h2>", unsafe_allow_html=True)
about_cols = st.columns(3)
about_data = [
    ("🔍", "Advanced Analytics", "QuantPilot leverages cutting-edge algorithms to analyze financial data with precision, uncovering hidden patterns and opportunities."),
    ("🤖", "AI-Powered", "Our machine learning models continuously learn from market data to provide increasingly accurate predictions and insights."),
    ("📊", "Visual Intelligence", "Complex financial data transformed into intuitive visualizations that tell the story behind the numbers.")
]
for i, col in enumerate(about_cols):
    with col:
        st.markdown(f"""
            <div class="feature-card" style="min-height: 210px;">
                <div style="font-size: 2.1rem;">{about_data[i][0]}</div>
                <div class="feature-title">{about_data[i][1]}</div>
                <p style="color: #323338">{about_data[i][2]}</p>
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
            icon, title, desc = features[i + j]
            with cols[j]:
                st.markdown(f"""
                    <div class="feature-card">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <p style="color: #323338">{desc}</p>
                    </div>
                """, unsafe_allow_html=True)

# Contact Section
st.markdown("<h2 class='section-title'>Contact</h2>", unsafe_allow_html=True)
st.markdown("""
    <div class="feature-card" style="text-align:center;">
        <p>Have questions or feedback?</p>
        <p>Email us at <a href="mailto:team@quantpilot.ai">team@quantpilot.ai</a></p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
""", unsafe_allow_html=True)