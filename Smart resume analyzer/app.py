import streamlit as st
import os
from utils.db import init_db

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Smart AI Resume Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database Schema & Seed Data
init_db()

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Branding
st.sidebar.image("https://img.icons8.com/isometric-folders/100/resume.png", width=70)
st.sidebar.title("Smart AI Resume")
st.sidebar.caption("v2.5 • All-in-One AI Career Suite")
st.sidebar.markdown("---")

# Main Home Landing Page
st.markdown('<div class="hero-title">Smart AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Optimize your resume with AI-driven ATS scoring, keyword gap diagnostics, tailored feedback, and multi-theme PDF builders.</div>', unsafe_allow_html=True)

# Quick Stats Banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="metric-box">
            <div class="metric-val">98.4%</div>
            <div class="metric-lbl">ATS Accuracy Rate</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-box">
            <div class="metric-val">4 Themes</div>
            <div class="metric-lbl">Exportable PDF Templates</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-box">
            <div class="metric-val">Gemini AI</div>
            <div class="metric-lbl">Optimization Engine</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="metric-box">
            <div class="metric-val">Instant</div>
            <div class="metric-lbl">Report PDF Export</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Core Feature Cards Showcase
st.markdown('<div class="section-header">Explore Modules</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="glass-card">
            <h3>🔍 Resume Analyzer</h3>
            <p style="color:#94A3B8;">Upload your PDF or Word resume to get an instant ATS score, visual skill gap breakdowns, course & video suggestions, and downloadable PDF reports.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Analyzer ➔", key="btn_analyzer"):
        st.switch_page("pages/1_🔍_Resume_Analyzer.py")

with c2:
    st.markdown("""
        <div class="glass-card">
            <h3>📝 Resume Builder</h3>
            <p style="color:#94A3B8;">Craft an ATS-optimized resume from scratch or import existing data. Powered by Gemini AI bullet suggestions with 4 sleek visual themes.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Resume Builder ➔", key="btn_builder"):
        st.switch_page("pages/2_📝_Resume_Builder.py")

with c3:
    st.markdown("""
        <div class="glass-card">
            <h3>📊 User Dashboard</h3>
            <p style="color:#94A3B8;">Track your ATS score progress over time, review historical resume analyses, and access saved resume drafts with interactive charts.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("View Dashboard ➔", key="btn_dashboard"):
        st.switch_page("pages/3_📊_Dashboard.py")

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
        <div class="glass-card">
            <h3>🎯 Job Search</h3>
            <p style="color:#94A3B8;">Explore real-time LinkedIn job opportunities, market skill trends, salary insights, and top hiring tech companies.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Search Jobs ➔", key="btn_jobs"):
        st.switch_page("pages/4_🎯_Job_Search.py")

with c5:
    st.markdown("""
        <div class="glass-card">
            <h3>💬 User Feedback</h3>
            <p style="color:#94A3B8;">Share your thoughts, suggestions, and ratings to help improve the Smart AI Resume Analyzer platform.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Give Feedback ➔", key="btn_feedback"):
        st.switch_page("pages/5_💬_Feedback.py")

with c6:
    st.markdown("""
        <div class="glass-card">
            <h3>🔐 Admin Analytics</h3>
            <p style="color:#94A3B8;">Login-gated administrative suite for system metrics, feedback management, user score distributions, and usage stats.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Admin Portal ➔", key="btn_admin"):
        st.switch_page("pages/7_🔐_Admin.py")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Smart AI Resume Analyzer • Powered by Streamlit, spaCy, and Google Gemini API • Released under MIT License")
