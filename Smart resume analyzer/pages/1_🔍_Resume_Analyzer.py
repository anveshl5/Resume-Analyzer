import streamlit as st
import os
import plotly.graph_objects as go
import plotly.express as px
from utils.resume_parser import parse_resume
from utils.ats_scorer import compute_ats_score, get_highlighted_text, ROLE_SKILL_MAP
from utils.ai_engine import generate_ai_suggestions, get_role_insights
from utils.pdf_export import generate_analysis_report_pdf
from utils.db import save_analysis

st.set_page_config(page_title="Resume Analyzer • Smart AI", page_icon="🔍", layout="wide")

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero-title">🔍 Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Upload your resume for comprehensive ATS scoring, keyword gap diagnostics, and AI-powered recommendations.</div>', unsafe_allow_html=True)

# Layout Setup: Left Controls, Right Results
col_control, col_display = st.columns([1, 2])

with col_control:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("1. Target Role & Settings")
    
    role_options = list(ROLE_SKILL_MAP.keys())
    target_role = st.selectbox("Select Target Job Role:", role_options, index=0)

    use_custom_jd = st.checkbox("Use Custom Job Description (JD)")
    custom_jd_text = ""
    if use_custom_jd:
        custom_jd_text = st.text_area("Paste Target Job Description:", height=150, placeholder="Paste the job requirements, responsibilities, and qualifications here...")

    st.subheader("2. Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF or Word file:", type=["pdf", "docx"])
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_display:
    if uploaded_file is not None:
        with st.spinner("Analyzing resume content with spaCy NLP and ATS Engine..."):
            parsed_data = parse_resume(uploaded_file)
            ats_result = compute_ats_score(parsed_data, target_role, custom_jd_text)
            
            # Save analysis to database
            save_analysis(
                filename=parsed_data["filename"],
                target_role=target_role,
                ats_score=ats_result["overall_score"],
                present_skills_count=len(ats_result["present_skills"]),
                missing_skills_count=len(ats_result["missing_skills"])
            )

        st.success(f"Successfully analyzed **{parsed_data['filename']}**!")

        # Top Metric Gauge & Overview
        m1, m2 = st.columns([1, 1])

        with m1:
            # Plotly ATS Score Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=ats_result["overall_score"],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "ATS Score", 'font': {'size': 20, 'color': '#F8FAFC'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                    'bar': {'color': "#6366F1"},
                    'bgcolor': "rgba(30, 41, 59, 0.5)",
                    'borderwidth': 2,
                    'bordercolor': "#334155",
                    'steps': [
                        {'range': [0, 50], 'color': '#EF4444'},
                        {'range': [50, 75], 'color': '#F59E0B'},
                        {'range': [75, 100], 'color': '#10B981'}
                    ],
                }
            ))
            fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gauge, use_container_width=True)

        with m2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"### Score Breakdown")
            st.markdown(f"• **Skill Match:** {ats_result['skill_score']}%")
            st.markdown(f"• **Content Relevance:** {ats_result['similarity_score']}%")
            st.markdown(f"• **Formatting & Contact Info:** {ats_result['format_score']}%")
            st.markdown(f"• **Detected Email:** `{parsed_data['email']}`")
            st.markdown(f"• **Detected Phone:** `{parsed_data['phone']}`")
            st.markdown(f"• **Word Count:** {parsed_data['word_count']} words")
            st.markdown('</div>', unsafe_allow_html=True)

        # Tabs for detailed insights
        tab_skills, tab_feedback, tab_recs, tab_report, tab_raw = st.tabs([
            "📊 Skills Gap Analysis", 
            "💡 AI Role Feedback", 
            "🎓 Courses & Videos", 
            "📄 Export PDF Report",
            "📝 Highlighted Resume Text"
        ])

        with tab_skills:
            st.subheader("Missing vs Present Skills")
            p_len = len(ats_result["present_skills"])
            m_len = len(ats_result["missing_skills"])

            fig_pie = px.pie(
                values=[p_len, m_len],
                names=["Present Skills", "Missing Skills"],
                color_discrete_sequence=["#10B981", "#EF4444"],
                hole=0.4,
                title=f"Skills Coverage for {target_role}"
            )
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC")
            st.plotly_chart(fig_pie, use_container_width=True)

            c_pres, c_miss = st.columns(2)
            with c_pres:
                st.markdown("#### ✅ Present Skills")
                if ats_result["present_skills"]:
                    for s in ats_result["present_skills"]:
                        st.markdown(f"- `<span class='highlight-kw'>{s}</span>`", unsafe_allow_html=True)
                else:
                    st.info("No matching target skills detected.")

            with c_miss:
                st.markdown("#### ❌ Missing / Recommended Skills")
                if ats_result["missing_skills"]:
                    for s in ats_result["missing_skills"]:
                        st.markdown(f"- **{s}**")
                else:
                    st.success("Great job! All key skills are present.")

        with tab_feedback:
            st.subheader(f"AI Feedback Tailored for {target_role}")
            with st.spinner("Generating role-specific AI insights..."):
                prompt = f"Give 3 tailored action items to improve a resume for a {target_role} role. Mention present skills {ats_result['present_skills']} and missing skills {ats_result['missing_skills']}."
                ai_feedback = generate_ai_suggestions(prompt)
                st.markdown(ai_feedback)

            st.markdown("---")
            st.subheader("Industry Insights")
            insights = get_role_insights(target_role)
            st.info(insights)

        with tab_recs:
            st.subheader(f"Recommended Courses for {target_role}")
            for course in ats_result["courses"]:
                st.markdown(f"🎓 **[{course['title']}]({course['url']})** — *{course['provider']}*")
            
            st.markdown("---")
            st.subheader("Curated Video Guides")
            for vid in ats_result["videos"]:
                st.markdown(f"📺 **[{vid['title']}]({vid['url']})** — *Channel: {vid['channel']}*")

        with tab_report:
            st.subheader("AI-Generated PDF Analysis Report")
            st.write("Download a formatted PDF summary of your ATS score, detected skills gap, and recommendations.")
            pdf_bytes = generate_analysis_report_pdf(ats_result, parsed_data["filename"])
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"ATS_Report_{parsed_data['filename']}.pdf",
                mime="application/pdf"
            )

        with tab_raw:
            st.subheader("Parsed Text with Keyword Highlighting")
            highlighted_html = get_highlighted_text(parsed_data["raw_text"], ats_result["present_skills"])
            st.markdown(f"<div class='glass-card' style='max-height:400px; overflow-y:auto; font-family:monospace; white-space:pre-wrap;'>{highlighted_html}</div>", unsafe_allow_html=True)

    else:
        st.info("👆 Upload a PDF or Word resume on the left control panel to see live ATS scoring and analytics.")
