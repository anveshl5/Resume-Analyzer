import streamlit as st
import os

st.set_page_config(page_title="About • Smart AI", page_icon="ℹ️", layout="wide")

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero-title">ℹ️ About Smart AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">An end-to-end open-source suite for intelligent resume diagnostics and career optimization.</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="glass-card">
        <h3>🚀 Product Overview</h3>
        <p style="color:#94A3B8; line-height:1.7;">
            <b>Smart AI Resume Analyzer</b> empowers job seekers to optimize their resumes for Automated Applicant Tracking Systems (ATS). 
            By combining deterministic Natural Language Processing (spaCy NLP) with Google Gemini AI models, the application analyzes keyword relevance, 
            skills gaps, document structure, and role readiness — providing actionable recommendations, visual charts, and downloadable PDF reports.
        </p>
    </div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="glass-card">
            <h3>🛠️ Tech Stack & Architecture</h3>
            <ul>
                <li><b>Framework:</b> Streamlit (Multi-page app with custom CSS glassmorphism)</li>
                <li><b>Backend Engine:</b> Python 3.10+</li>
                <li><b>NLP & Entity Extraction:</b> spaCy (en_core_web_sm model)</li>
                <li><b>Generative AI:</b> Google Gemini API (via google-generativeai)</li>
                <li><b>PDF & DOCX Parsing:</b> pdfplumber & python-docx</li>
                <li><b>PDF Export Generator:</b> ReportLab Engine</li>
                <li><b>Database Store:</b> SQLite (Local file-based store)</li>
                <li><b>Data Visualizations:</b> Plotly & Pandas</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="glass-card">
            <h3>⚖️ License & Open Source</h3>
            <p style="color:#94A3B8;">
                Distributed under the <b>MIT License</b>. Free for personal, academic, and commercial application development.
            </p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <h4>📄 MIT License Summary</h4>
            <p style="color:#94A3B8; font-size:0.9rem;">
                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files...
            </p>
        </div>
    """, unsafe_allow_html=True)
