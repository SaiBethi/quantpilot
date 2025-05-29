import streamlit as st

# Improved hero description
hero_description = (
    "Level up your investing with QuantPilot: AI-powered analytics, real-time visualizations, and actionable insights. "
    "Transform complexity into clarity and make every decision count—no matter your experience level."
)

# --- SIDE NAVIGATION (BETTER VISIBILITY & LAYOUT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    .side-nav-container {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 72px;
        z-index: 99999 !important;
        background: rgba(255,255,255,0.99);
        box-shadow: 4px 0 28px -8px rgba(31,41,55,0.20), 1px 0 0 0 #e3eaf5;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        transition: width 0.25s cubic-bezier(.18,.89,.32,1.28);
        border-right: 2px solid #e3eaf5;
    }
    .side-nav-container.expanded {
        width: 220px;
    }
    .nav-toggle {
        margin-top: 1.3em;
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
    @media (min-width: 640px) {
        .side-nav-container.expanded .side-nav-links { opacity: 1; pointer-events: auto; }
        .side-nav-links { opacity: 1 !important; pointer-events: auto !important; }
    }
    .side-nav-link {
        font-family: 'EB Garamond', serif !important;
        color: #1a1b1f;
        font-size: 1.17rem;
        font-weight: 600;
        text-decoration: none;
        margin: 0.61em 0 0.61em 0.5em;
        padding: 0.27em 1em 0.27em 0.65em;
        border-radius: 8px 30px 30px 8px;
        transition: background 0.16s, color 0.18s, box-shadow 0.18s;
        letter-spacing: 0.01em;
        border-left: 3.5px solid transparent;
        width: 91%;
        display: flex;
        align-items: center;
        cursor: pointer;
        opacity: 0.97;
        box-shadow: none;
        background: none;
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
    /* Always show links on large screens */
    @media (min-width: 640px) {
        .side-nav-container.expanded .side-nav-links { opacity: 1; pointer-events: auto; }
        .side-nav-links { opacity: 1 !important; pointer-events: auto !important; }
    }
    /* Make room for nav: */
    .stApp { margin-left: 76px !important; transition: margin-left 0.25s cubic-bezier(.18,.89,.32,1.28);}
    .side-nav-container.expanded ~ .stApp { margin-left: 224px !important; }
    @media (max-width: 700px) {
        .side-nav-container { width: 48px; }
        .side-nav-link { font-size: 1.00rem; }
        .stApp { margin-left: 52px !important; }
        .side-nav-container.expanded { width: 90vw; }
        .side-nav-container.expanded ~ .stApp { margin-left: 90vw !important; }
        .side-nav-links { font-size: 1.12rem; }
    }
    body { overflow-x: visible !important; }
    </style>
    <script>
    window.addEventListener('DOMContentLoaded', function() {
        let nav = document.querySelector('.side-nav-container');
        let toggle = document.querySelector('.nav-toggle');
        if (toggle && nav) {
            toggle.onclick = function() {
                nav.classList.toggle('expanded');
                let app = document.querySelector('.stApp');
                if (nav.classList.contains('expanded')) {
                    app.style.marginLeft = window.innerWidth < 700 ? '90vw' : '224px';
                } else {
                    app.style.marginLeft = window.innerWidth < 700 ? '52px' : '76px';
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
            <a class="side-nav-link" href="#home"><span class="side-nav-label">Home</span></a>
            <a class="side-nav-link" href="/dashboard" target="_self"><span class="side-nav-label">Dashboard</span></a>
            <a class="side-nav-link" href="#ai-insights"><span class="side-nav-label">AI Insights</span></a>
            <a class="side-nav-link" href="#about"><span class="side-nav-label">About</span></a>
            <a class="side-nav-link" href="#contact"><span class="side-nav-label">Contact</span></a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- END SIDE NAV ---

# The rest of your app as before...

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