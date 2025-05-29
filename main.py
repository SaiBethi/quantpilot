import streamlit as st

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Handle custom navigation clicks
def navigate(page_name):
    st.session_state.page = page_name

# ----- FIXED SIDEBAR NAVIGATION -----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;700&display=swap');

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
        font-family: 'EB Garamond', serif;
    }
    .custom-left-nav button {
        all: unset;
        display: block;
        color: #2a2d44;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 18px 0;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
        padding: 8px;
        text-align: center;
        width: 56px;
        border-radius: 10px;
    }
    .custom-left-nav button:hover, .custom-left-nav button.selected {
        background: #e4eafc;
        color: #1946d2;
    }
    .stApp {
        margin-left: 80px;
    }
    </style>
    <div class="custom-left-nav">
        <form action="" method="post">
            <button name="page" type="submit" value="home" class="{home_class}">🏠</button>
            <button name="page" type="submit" value="dashboard" class="{dashboard_class}">📊</button>
            <button name="page" type="submit" value="ai" class="{ai_class}">🤖</button>
            <button name="page" type="submit" value="about" class="{about_class}">📚</button>
            <button name="page" type="submit" value="contact" class="{contact_class}">✉️</button>
        </form>
    </div>
""".format(
    home_class="selected" if st.session_state.page == "home" else "",
    dashboard_class="selected" if st.session_state.page == "dashboard" else "",
    ai_class="selected" if st.session_state.page == "ai" else "",
    about_class="selected" if st.session_state.page == "about" else "",
    contact_class="selected" if st.session_state.page == "contact" else "",
), unsafe_allow_html=True)

# Handle navigation post request
if st.session_state.get("_submitted_form_data"):
    st.session_state.page = st.session_state._submitted_form_data.get("page", "home")

# ----- PAGE CONTENT -----
st.markdown(f"<div style='padding: 2rem; font-family: EB Garamond, serif;'>", unsafe_allow_html=True)

if st.session_state.page == "home":
    st.title("🏠 Welcome to QuantPilot")
    st.write("Level up your investing with AI-powered insights, real-time charts, and more.")

elif st.session_state.page == "dashboard":
    st.title("📊 Dashboard")
    st.write("Here’s where your real-time financial data and visualizations will live.")

elif st.session_state.page == "ai":
    st.title("🤖 AI Insights")
    st.write("Get personalized insights powered by machine learning.")

elif st.session_state.page == "about":
    st.title("📚 About QuantPilot")
    st.write("QuantPilot simplifies investing with intelligent tools designed for clarity and confidence.")

elif st.session_state.page == "contact":
    st.title("✉️ Contact Us")
    st.write("Questions or feedback? Reach out to the QuantPilot team!")

st.markdown("</div>", unsafe_allow_html=True)