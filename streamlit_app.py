import streamlit as st

hero_description = (
    "Level up your investing with QuantPilot: AI-powered analytics, real-time visualizations, and actionable insights. "
    "Transform complexity into clarity and make every decision count—no matter your experience level."
)

# --- FIXED, MINIMAL, VISIBLE LEFT SIDEBAR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

    /* Sidebar styling */
    .custom-left-nav {
        position: fixed;
        top: 0; left: 0;
        width: 80px;
        height: 100vh;
        background: rgba(255,255,255,0.97);
        border-right: 2px solid #e3eaf5;
        box-shadow: 4px 0 24px -8px rgba(31,41,55,0.13);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 32px;
        font-family: 'EB Garamond', serif !important;
    }
    .custom-left-nav a {
        display: block;
        color: #2a2d44;
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 18px 0;
        padding: 10px 7px;
        border-radius: 10px;
        transition: background 0.15s, color 0.15s;
        text-align: center;
        width: 56px;
        letter-spacing: 0.01em;
    }
    .custom-left-nav a:hover, .custom-left-nav a.active {
        background: #e4eafc;
        color: #1946d2;
    }
    .custom-left-nav .nav-icon {
        font-size: 1.4em;
        display: block;
        margin-bottom: 2px;
    }
    /* Move all Streamlit content to the right! */
    .stApp {
        margin-left: 80px !important;
    }
    @media (max-width: 600px) {
        .custom-left-nav { width: 56px; }
        .stApp { margin-left: 56px !important; }
        .custom-left-nav a { font-size: 1.1rem; width: 40px; padding: 7px 2px; }
    }
    </style>
    <nav class="custom-left-nav">
        <a href="#home" title="Home"><span class="nav-icon">🏠</span></a>
        <a href="/dashboard" title="Dashboard" target="_self"><span class="nav-icon">📊</span></a>
        <a href="#ai-insights" title="AI Insights"><span class="nav-icon">🤖</span></a>
        <a href="#about" title="About"><span class="nav-icon">📚</span></a>
        <a href="#contact" title="Contact"><span class="nav-icon">✉️</span></a>
    </nav>
""", unsafe_allow_html=True)

# --- END SIDEBAR ---

# Main content below (unchanged!):

st.markdown("""
<a id="home"></a>
<div class="hero">
    <div class="hero-title" style="margin-bottom:0.45em;">📈 QuantPilot</div>
    <div class="hero-desc">{}</div>
    <div>
        <a href="/dashboard" target="_self" style="text-decoration: none;">
            <button class="dash-btn">Launch Dashboard</button>
        </a>
    </div>
</div>
""".format(hero_description), unsafe_allow_html=True)

st.markdown("""
<a id="about"></a>
<div style="text-align:center;">
    <div class="section-label">Our Approach</div>
</div>
""", unsafe_allow_html=True)

about_cols = st.columns(3)
about_data = [
    ("🔍", "Advanced Analytics", "QuantPilot leverages advanced algorithms to analyze financial data with precision, uncovering hidden patterns and opportunities."),
    ("🤖", "AI-Powered", "Our machine learning models continuously learn from evolving market data, offering ever-more accurate predictions and insights."),
    ("📊", "Visual Intelligence", "Complex financials transformed into beautiful, intuitive visuals—making trends and outliers instantly clear.")
]
for i, col in enumerate(about_cols):
    with col:
        st.markdown(f"""
            <div class="feature-card" style="min-height: 210px;">
                <div class="feature-title">{about_data[i][1]}</div>
                <div style="font-size: 2.1rem; margin-bottom:0.25em;">{about_data[i][0]}</div>
                <p style="color: #191c24;">{about_data[i][2]}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
<a id="ai-insights"></a>
<div style="text-align:center; margin-top:2.5em;">
    <div class="section-label">Key Features</div>
</div>
""", unsafe_allow_html=True)
features = [
    ("📉", "Interactive Charts", "Dynamic, zoomable charts that update in real-time as you explore and adjust parameters—making your data come alive."),
    ("🧠", "AI Predictions", "Forward-looking market forecasts powered by proprietary AI models trained on decades of financial data."),
    ("📈", "Technical Indicators", "Analyze trends with pro-grade indicators: RSI, MACD, Bollinger Bands, and more—no spreadsheet required."),
    ("📋", "Stock Summary", "Glanceable dashboards with key metrics like PE ratio, market cap, and dividend yield for quick, smart decisions."),
    ("📁", "Downloadable Reports", "Export insights as beautiful, ready-to-share CSV files for your workflow, meetings, or research.")
]
for i in range(0, len(features), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(features):
            icon, title, desc = features[i + j]
            with cols[j]:
                st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-title">{title}</div>
                        <div style="font-size: 2rem; margin-bottom:0.25em;">{icon}</div>
                        <p style="color: #191c24;">{desc}</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("""
<a id="contact"></a>
<div style="text-align:center; margin-top:2.5em;">
    <div class="section-label">Get in Touch</div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
    <div class="feature-card" style="text-align:center;">
        <p style="color:#191c24;">Questions? Feedback? We're here to help you succeed.</p>
        <p style="color:#191c24;">Email us at <a href="mailto:team@quantpilot.ai">team@quantpilot.ai</a></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
""", unsafe_allow_html=True)