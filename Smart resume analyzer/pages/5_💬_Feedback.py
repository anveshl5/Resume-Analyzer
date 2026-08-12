import streamlit as st
import os
from utils.db import save_feedback

st.set_page_config(page_title="Feedback • Smart AI", page_icon="💬", layout="wide")

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero-title">💬 User Feedback & Community Ratings</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Your feedback shapes the future of Smart AI Resume Analyzer. Let us know how we can improve!</div>', unsafe_allow_html=True)

col_form, col_info = st.columns([2, 1])

with col_form:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Submit Your Feedback")

    with st.form("feedback_form", clear_on_submit=True):
        fb_name = st.text_input("Your Name:", placeholder="Alex Mercer")
        fb_email = st.text_input("Email Address:", placeholder="alex@example.com")
        
        user_role = st.selectbox("I am a:", ["Job Seeker", "Recruiter / Hiring Manager", "Student", "Career Coach", "Developer / Other"])
        rating = st.slider("Rating (1 to 5 Stars):", min_value=1, max_value=5, value=5)
        
        feedback_text = st.text_area("Feedback / Suggestions / Feature Requests:", height=140, placeholder="Tell us what features you loved or what we should add next...")
        
        submitted = st.form_submit_button("🚀 Submit Feedback")
        
        if submitted:
            if not fb_name or not fb_email or not feedback_text:
                st.error("Please fill in your name, email, and feedback message.")
            else:
                save_feedback(fb_name, fb_email, user_role, rating, feedback_text)
                st.success("🎉 Thank you! Your feedback has been saved successfully.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    st.markdown("""
        <div class="glass-card">
            <h3>🌟 Why Your Feedback Matters</h3>
            <p style="color:#94A3B8;">We continuously update our ATS keyword scoring algorithms, spaCy NLP parsers, and report templates based directly on user suggestions.</p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <h4>🔒 Privacy Assurance</h4>
            <p style="color:#94A3B8;">Your data is stored locally in your SQLite database instance and is never sold to third parties.</p>
        </div>
    """, unsafe_allow_html=True)
