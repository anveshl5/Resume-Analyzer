import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils.db import get_all_analyses

st.set_page_config(page_title="Dashboard • Smart AI", page_icon="📊", layout="wide")

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero-title">📊 Analytics & History Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Track your ATS score progress over time, review historical analyses, and examine performance metrics.</div>', unsafe_allow_html=True)

# Fetch History from SQLite
rows = get_all_analyses()

if not rows:
    st.info("No analysis history recorded yet. Head over to 🔍 Resume Analyzer to scan your first resume!")
else:
    df = pd.DataFrame([dict(r) for r in rows])
    df['analyzed_at'] = pd.to_datetime(df['analyzed_at'])

    # KPI Top Metric Cards
    total_scans = len(df)
    avg_score = round(df['ats_score'].mean(), 1)
    best_score = round(df['ats_score'].max(), 1)
    latest_role = df.iloc[0]['target_role'] if total_scans > 0 else "N/A"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{total_scans}</div>
                <div class="metric-lbl">Total Scans</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{avg_score}%</div>
                <div class="metric-lbl">Average Score</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{best_score}%</div>
                <div class="metric-lbl">Highest ATS Score</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="font-size:1.4rem; font-weight:600;">{latest_role}</div>
                <div class="metric-lbl">Latest Target Role</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Trend & Distribution Charts
    c_trend, c_role = st.columns([3, 2])

    with c_trend:
        st.subheader("📈 ATS Score Improvement Trend")
        fig_trend = px.line(
            df.sort_values("analyzed_at"),
            x="analyzed_at",
            y="ats_score",
            markers=True,
            text="ats_score",
            labels={"analyzed_at": "Scan Date", "ats_score": "ATS Score (%)"}
        )
        fig_trend.update_traces(line_color="#6366F1", line_width=3, marker_size=8)
        fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", yaxis_range=[0, 100])
        st.plotly_chart(fig_trend, use_container_width=True)

    with c_role:
        st.subheader("🎯 Target Role Distribution")
        fig_bar = px.bar(
            df['target_role'].value_counts().reset_index(),
            x="target_role",
            y="count",
            color="target_role",
            labels={"target_role": "Target Role", "count": "Count"}
        )
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("📜 Detailed Analysis Log History")
    
    st.dataframe(
        df[["id", "filename", "target_role", "ats_score", "present_skills_count", "missing_skills_count", "analyzed_at"]],
        use_container_width=True,
        column_config={
            "id": "Scan ID",
            "filename": "Filename",
            "target_role": "Target Role",
            "ats_score": st.column_config.NumberColumn("ATS Score (%)", format="%.1f%%"),
            "present_skills_count": "Matched Skills",
            "missing_skills_count": "Missing Skills",
            "analyzed_at": "Timestamp"
        }
    )
