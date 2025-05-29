import streamlit as st

# Enhanced hero description
hero_description = (
    "Unlock smarter investing with QuantPilot — your AI-powered co-pilot for financial markets. "
    "Dive into advanced analytics, gain crystal-clear insights, and visualize opportunities in real time. "
    "From active traders to curious beginners, QuantPilot transforms raw data into intelligent, actionable strategies."
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'EB Garamond', serif !important;
        background:
            linear-gradient(120deg, rgba(25, 28, 36, 0.68) 60%, rgba(31,84,193, 0.18) 100%),
            url('https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2015&q=80') no-repeat center center fixed;
        background-size: cover !important;
        background-attachment: fixed !important;
        min-height: 100vh;
    }
    .main, .stApp { background: transparent !important; }
    .logo-container {
        text-align: center;
        margin: 2.2vw auto 0.5vw auto;
    }
    .logo-img {
        width: min(150px, 18vw);
        max-width: 180px;
        border-radius: 22px;
        background: #fff;
        box-shadow: 0 12px 36px -5px rgba(30,50,130,0.19);
        border: 2.5px solid #fff;
        margin-bottom: 0.7em;
        transition: transform 0.21s cubic-bezier(.18,.89,.32,1.28), box-shadow 0.22s;
    }
    .logo-img:hover {
        transform: scale(1.04) rotate(-1.4deg);
        box-shadow: 0 16px 48px -10px rgba(31,41,55,0.22);
    }
    .hero {
        color: #191c24;
        text-align: center;
        background: rgba(0,0,0,0.00);
        box-shadow: none;
        margin-bottom: 2.4vw;
    }
    .hero-title {
        font-family: 'EB Garamond', serif !important;
        font-size: min(8vw, 3.2rem);
        font-weight: bold;
        margin-bottom: 0.1em;
        color: #191c24;
        background: rgba(255,255,255,0.97);
        display: inline-block;
        padding: 0.28em 1.35em 0.18em 1.35em;
        border-radius: 18px;
        box-shadow: 0 8px 24px -10px rgba(31,41,55,0.13);
        transition: box-shadow 0.22s, transform 0.22s;
        letter-spacing: 0.03em;
    }
    .hero-title:hover {
        box-shadow: 0 18px 44px -15px rgba(31,41,55,0.20);
        transform: translateY(-3px) scale(1.03);
    }
    .hero-desc {
        font-family: 'EB Garamond', serif !important;
        font-size: min(3vw, 1.21rem);
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
        text-shadow: 0 1px 0.5px #fff7;
        letter-spacing: 0.01em;
    }
    .hero-desc:hover {
        box-shadow: 0 12px 36px -12px rgba(31,41,55,0.17);
        transform: scale(1.022);
    }
    .section-label {
        display: inline-block;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.27rem;
        font-weight: 600;
        color: #191c24;
        background: #fff;
        border-radius: 11px;
        padding: 0.16em 1.15em 0.09em 1.15em;
        margin-bottom: 0.6em;
        letter-spacing: 0.02em;
        box-shadow: 0 7px 22px -10px rgba(31,41,55,0.13);
        transition: box-shadow 0.22s, transform 0.22s;
        border: 1.5px solid #e8edf5;
    }
    .section-label:hover {
        box-shadow: 0 16px 36px -14px rgba(31,41,55,0.20);
        transform: scale(1.037);
    }
    .section-title {
        text-align: center;
        font-size: 2.1rem;
        margin: 0.2rem 0 1.6rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        color: #191c24;
        font-family: 'EB Garamond', serif !important;
        background: none;
        text-shadow: none;
    }
    .feature-card {
        background: rgba(255,255,255,0.99);
        color: #101113;
        padding: 2rem 1.4rem;
        margin-bottom: 1.6rem;
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
        .section-title { font-size: 1.3rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Logo (centered, looks best above the hero)
st.markdown("""
    <div class="logo-container">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAGQCAYAAACZyyqOAAABFUlEQVR4nO3BMQEAAAgDoJvcq1/kM4MGOGpAAAAAAAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAB4ENgAAMAHgQ2AAAwAeBDYAADAHgQ2AADc6LqjAAEBAAAAAElFTkSuQmCC" class="logo-img" alt="QuantPilot Logo">
    </div>
""", unsafe_allow_html=True)
st.image("image2", use_column_width=False, width=180, output_format="auto")

# Hero Section
st.markdown("""
    <div class="hero">
        <div class="hero-title" style="margin-bottom:0.45em;">QuantPilot</div>
        <div></div>
        <div class="hero-desc">{}</div>
        <div>
            <a href="/dashboard" target="_self" style="text-decoration: none;">
                <button class="dash-btn">Launch Dashboard</button>
            </a>
        </div>
    </div>
""".format(hero_description), unsafe_allow_html=True)

# Our Approach Section
st.markdown("""
    <div style="text-align:center;">
        <div class="section-label">Our Approach</div>
    </div>
    <h2 class='section-title'>Empowering Investors Through Intelligence</h2>
""", unsafe_allow_html=True)

about_cols = st.columns(3)
about_data = [
    ("🔍", "Advanced Analytics", "Harness deep-learning and statistical models for precision analysis—unearthing market trends and opportunities hidden in the data."),
    ("🤖", "AI-Powered", "Continuous learning from global market data fuels ever-improving predictions and adaptive insights tailored to your portfolio."),
    ("📊", "Visual Intelligence", "Complex financial data is transformed into interactive, intuitive visuals that make trends and outliers immediately clear.")
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

# Key Features Section
st.markdown("""
    <div style="text-align:center; margin-top:2.5em;">
        <div class="section-label">Key Features</div>
    </div>
    <h2 class='section-title'>How QuantPilot Elevates Your Investment Experience</h2>
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

# Get in Touch Section
st.markdown("""
    <div style="text-align:center; margin-top:2.5em;">
        <div class="section-label">Get in Touch</div>
    </div>
    <h2 class='section-title'>Let's Build Your Financial Edge</h2>
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