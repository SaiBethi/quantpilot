import streamlit as st

# Improved hero description
hero_description = (
    "Level up your investing with QuantPilot: AI-powered analytics, real-time visualizations, and actionable insights. "
    "Transform complexity into clarity and make every decision count—no matter your experience level."
)

# --- SIDE NAVIGATION (collapsible, always visible, modern) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    /* Side Nav */
    .side-nav-container {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 62px;
        z-index: 9999;
        background: rgba(255,255,255,0.94);
        box-shadow: 2px 0 20px -8px rgba(31,41,55,0.13);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        transition: width 0.22s cubic-bezier(.18,.89,.32,1.28);
    }
    .side-nav-container.expanded {
        width: 210px;
    }
    .nav-toggle {
        margin-top: 1.4em;
        margin-bottom: 1.6em;
        cursor: pointer;
        background: none;
        border: none;
        padding: 7px;
        border-radius: 7px;
        transition: background 0.17s;
    }
    .nav-toggle:hover {
        background: #e7eaf6;
    }
    .dot-icon {
        width: 26px;
        height: 26px;
        display: inline-block;
        fill: #3b446a;
        margin-left: 2px;
    }
    .side-nav-links {
        margin-top: 2.6em;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.22s;
        padding-left: 2px;
    }
    .side-nav-container.expanded .side-nav-links {
        opacity: 1;
        pointer-events: auto;
    }
    .side-nav-link {
        font-family: 'EB Garamond', serif !important;
        color: #1a1b1f;
        font-size: 1.19rem;
        font-weight: 600;
        text-decoration: none;
        margin: 0.61em 0 0.61em 0.5em;
        padding: 0.22em 1em 0.22em 0.65em;
        border-radius: 8px 30px 30px 8px;
        transition: background 0.16s, color 0.18s, box-shadow 0.18s;
        letter-spacing: 0.01em;
        border-left: 3.5px solid transparent;
        width: 87%;
        display: flex;
        align-items: center;
        cursor: pointer;
        opacity: 0.92;
        box-shadow: none;
    }
    .side-nav-link:hover, .side-nav-link.active {
        background: linear-gradient(90deg, #e4eafc 75%, #f3f7ff 100%);
        color: #1946d2;
        border-left: 3.5px solid #1946d2;
        box-shadow: 0 2px 16px -8px #b9cfff55;
        text-decoration: none;
        opacity: 1.0;
    }
    .side-nav-label {
        margin-left: 0.7em;
        font-size: 1.0em;
        vertical-align: middle;
    }
    /* Make room for nav: */
    .stApp { margin-left: 62px !important; }
    .side-nav-container.expanded ~ .stApp { margin-left: 210px !important; }
    @media (max-width: 700px) {
        .side-nav-container { width: 46px; }
        .side-nav-container.expanded { width: 94vw; }
        .side-nav-link { font-size: 1.05rem; }
        .stApp { margin-left: 46px !important; }
        .side-nav-container.expanded ~ .stApp { margin-left: 94vw !important; }
    }
    </style>
    <script>
    // Collapsible side nav logic
    window.addEventListener('DOMContentLoaded', function() {
        let nav = document.querySelector('.side-nav-container');
        let toggle = document.querySelector('.nav-toggle');
        if (toggle && nav) {
            toggle.onclick = function() {
                nav.classList.toggle('expanded');
                // Adjust margin for app content
                let app = document.querySelector('.stApp');
                if (nav.classList.contains('expanded')) {
                    app.style.marginLeft = window.innerWidth < 700 ? '94vw' : '210px';
                } else {
                    app.style.marginLeft = window.innerWidth < 700 ? '46px' : '62px';
                }
            }
        }
    });
    </script>
    <div class="side-nav-container">
        <button class="nav-toggle" aria-label="Open navigation">
            <svg class="dot-icon" viewBox="0 0 32 32">
                <circle cx="6" cy="16" r="3"/>
                <circle cx="16" cy="16" r="3"/>
                <circle cx="26" cy="16" r="3"/>
            </svg>
        </button>
        <div class="side-nav-links">
            <a class="side-nav-link" href="#home">
                <span class="side-nav-label">Home</span>
            </a>
            <a class="side-nav-link" href="/dashboard" target="_self">
                <span class="side-nav-label">Dashboard</span>
            </a>
            <a class="side-nav-link" href="#ai-insights">
                <span class="side-nav-label">AI Insights</span>
            </a>
            <a class="side-nav-link" href="#about">
                <span class="side-nav-label">About</span>
            </a>
            <a class="side-nav-link" href="#contact">
                <span class="side-nav-label">Contact</span>
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- END SIDE NAV ---

# Global style for full-page background and EB Garamond font
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

# Hero Section (add anchor for nav)
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

# Our Approach Section (boxed label, nav anchor)
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

# Key Features Section (boxed label, nav anchor)
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

# Get in Touch Section (boxed label, nav anchor)
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

# Footer
st.markdown("""
    <div class="footer">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
""", unsafe_allow_html=True)