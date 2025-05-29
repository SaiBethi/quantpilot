import streamlit as st

# ---- FIXED, MINIMAL, NON-OVERLAPPING LEFT SIDEBAR ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

    /* Sidebar styling */
    .custom-left-nav {
        position: fixed;
        top: 0; left: 0;
        width: 80px;
        height: 100vh;
        background: rgba(255,255,255,0.98);
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

# ---- GLOBAL STYLES FOR THE WHOLE PAGE ----
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'EB Garamond', serif !important;
        scroll-behavior: smooth;
        background: 
            linear-gradient(110deg, rgba(25, 28, 36, 0.68) 60%, rgba(31,84,193, 0.18) 100%),
            url('https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2015&q=80') no-repeat center center fixed;
        background-size: cover !important;
        background-attachment: fixed !important;
        min-height: 100vh;
    }
    .main, .stApp {
        background: transparent !important;
    }
    .hero {
        color: #191c24;
        padding: 6vw 5vw 4vw 5vw;
        text-align: center;
        background: rgba(0,0,0,0.00);
        box-shadow: none;
    }
    .hero-title {
        font-family: 'EB Garamond', serif !important;
        font-size: min(10vw, 4rem);
        font-weight: bold;
        margin-bottom: 0.3em;
        color: #191c24;
        background: rgba(255,255,255,0.97);
        display: inline-block;
        padding: 0.38em 1.6em 0.18em 1.6em;
        border-radius: 18px;
        box-shadow: 0 8px 24px -10px rgba(31,41,55,0.13);
        transition: box-shadow 0.22s, transform 0.22s;
        letter-spacing: 0.03em;
    }
    .hero-title:hover {
        box-shadow: 0 18px 44px -15px rgba(31,41,55,0.20);
        transform: translateY(-4px) scale(1.03);
    }
    .hero-desc {
        font-family: 'EB Garamond', serif !important;
        font-size: min(4vw, 1.35rem);
        max-width: 700px;
        margin: 1.2rem auto 0.7em;
        color: #222b33;
        background: rgba(255,255,255,0.96);
        display: inline-block;
        padding: 0.65em 1.4em 0.65em 1.4em;
        border-radius: 12px;
        margin-bottom: 2.2rem;
        box-shadow: 0 6px 24px -8px rgba(31,41,55,0.10);
        transition: box-shadow 0.22s, transform 0.22s;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    .hero-desc:hover {
        box-shadow: 0 12px 36px -12px rgba(31,41,55,0.17);
        transform: scale(1.022);
    }
    .section-label {
        display: inline-block;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.29rem;
        font-weight: 600;
        color: #191c24;
        background: #fff;
        border-radius: 12px;
        padding: 0.18em 1.15em 0.10em 1.15em;
        margin-bottom: 1.05em;
        margin-top: 0.7em;
        letter-spacing: 0.02em;
        box-shadow: 0 7px 22px -10px rgba(31,41,55,0.13);
        transition: box-shadow 0.22s, transform 0.22s;
        border: 1.7px solid #e8edf5;
    }
    .section-label:hover {
        box-shadow: 0 16px 36px -14px rgba(31,41,55,0.20);
        transform: scale(1.037);
    }
    .feature-card {
        background: #fff;
        color: #191c24;
        padding: 2rem 1.4rem;
        margin-bottom: 1.7rem;
        border-radius: 18px;
        box-shadow: 0 10px 28px -6px rgba(31, 41, 55, 0.14), 0 2px 4px rgba(0,0,0,0.06);
        transition: transform 0.22s cubic-bezier(.18,.89,.32,1.28), box-shadow 0.22s, background 0.18s;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        z-index: 1;
        font-family: 'EB Garamond', serif !important;
        border: 1.5px solid #e4eaf2;
        backdrop-filter: blur(2px);
    }
    .feature-card:hover {
        transform: translateY(-7px) scale(1.048);
        box-shadow: 0 18px 36px -8px rgba(31,41,55,0.20), 0 4px 12px rgba(0,0,0,0.11);
        background: linear-gradient(104deg, #f8f6f3 60%, #f5f3ef 100%);
    }
    .feature-title {
        font-size: 1.27rem;
        font-weight: 700;
        margin-top: 0.7rem;
        margin-bottom: 0.45rem;
        color: #191c24;
        font-family: 'EB Garamond', serif !important;
        letter-spacing: 0.01em;
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
    @media (max-width: 900px) {
        .feature-card { font-size: 0.98rem; }
    }
    @media (max-width: 600px) {
        .feature-card { font-size: 0.93rem; padding: 1.3rem 0.7rem; }
        .section-label { font-size: 1.05rem; }
        .hero-title { font-size: 2rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ---- MAIN CONTENT ----

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