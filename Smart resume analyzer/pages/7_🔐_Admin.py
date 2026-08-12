import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils.db import verify_admin, get_admin_metrics, get_all_feedback, get_all_analyses

st.set_page_config(page_title="Admin Panel • Smart AI", page_icon="🔐", layout="wide")

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero-title">🔐 Administrative Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Login-gated administrative analytics, user feedback management, and system stats.</div>', unsafe_allow_html=True)

# Authentication Session State
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown('<div class="glass-card" style="max-width:500px; margin: 40px auto;">', unsafe_allow_html=True)
    st.subheader("Admin Authentication")
    
    with st.form("admin_login_form"):
        username_input = st.text_input("Username / Email:", value="admin@example.com")
        password_input = st.text_input("Password:", type="password", value="admin123")
        login_btn = st.form_submit_button("🔓 Log In")

        if login_btn:
            if verify_admin(username_input, password_input):
                st.session_state.admin_authenticated = True
                st.success("Authentication successful! Loading admin metrics...")
                st.rerun()
            else:
                st.error("Invalid credentials. Default: admin@example.com / admin123")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Admin Authenticated View
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("🔒 Logout Admin"):
        st.session_state.admin_authenticated = False
        st.rerun()

    metrics = get_admin_metrics()

    st.markdown("### 📈 System Usage & Aggregate Analytics")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{metrics['total_analyzed']}</div>
                <div class="metric-lbl">Total Resumes Analyzed</div>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{metrics['avg_score']}%</div>
                <div class="metric-lbl">Overall Average ATS Score</div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{metrics['total_feedback']}</div>
                <div class="metric-lbl">User Feedback Submissions</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_roles, col_scores = st.columns(2)

    with col_roles:
        st.subheader("Top Requested Job Roles")
        if metrics['top_roles']:
            roles_df = pd.DataFrame(metrics['top_roles'])
            fig_r = px.pie(roles_df, values="count", names="target_role", hole=0.3)
            fig_r.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC")
            st.plotly_chart(fig_r, use_container_width=True)
        else:
            st.info("No role metrics available.")

    with col_scores:
        st.subheader("Score Distribution Histogram")
        analyses = get_all_analyses()
        if analyses:
            df_a = pd.DataFrame([dict(a) for a in analyses])
            fig_hist = px.histogram(df_a, x="ats_score", nbins=10, color_discrete_sequence=["#10B981"])
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", xaxis_title="ATS Score Range (%)", yaxis_title="Count")
            st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    st.subheader("💬 User Feedback Submissions Log")
    feedback_rows = get_all_feedback()
    if feedback_rows:
        fb_df = pd.DataFrame([dict(r) for r in feedback_rows])
        st.dataframe(
            fb_df[["id", "name", "email", "user_role", "rating", "feedback_text", "submitted_at"]],
            use_container_width=True,
            column_config={
                "id": "ID",
                "name": "User Name",
                "email": "Email",
                "user_role": "User Category",
                "rating": st.column_config.NumberColumn("Rating", format="%d ⭐"),
                "feedback_text": "Feedback Message",
                "submitted_at": "Submitted At"
            }
        )
    else:
        st.info("No feedback submissions yet.")
