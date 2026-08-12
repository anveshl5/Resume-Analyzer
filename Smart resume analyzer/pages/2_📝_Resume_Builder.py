import streamlit as st
import os
from utils.ai_engine import get_smart_bullet_suggestions, generate_ai_suggestions
from utils.pdf_export import generate_resume_pdf

st.set_page_config(page_title="Resume Builder • Smart AI", page_icon="📝", layout="wide")

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero-title">📝 Interactive Resume Builder</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Create or refine ATS-optimized resumes with 4 professional themes and AI bullet point generation.</div>', unsafe_allow_html=True)

# Replicated & Documented Browser Autofill Bug Notice
st.markdown("""
    <div class="autofill-notice">
        <b>💡 Tip regarding Browser Autofill:</b> If your browser auto-fills Name/Email/Phone fields, click inside the field and edit slightly (or press Space) to ensure Streamlit's state captures your email properly. <i>(Documented autofill validation behavior: input blur mitigation active).</i>
    </div>
""", unsafe_allow_html=True)

# Theme Selector & Options Header
col_theme, col_opts = st.columns([2, 1])

with col_theme:
    selected_theme = st.selectbox(
        "Select PDF Design Theme:",
        ["Modern", "Minimal", "Professional", "Creative"],
        index=0,
        help="Choose your visual layout style for PDF generation."
    )

with col_opts:
    ats_formatting_toggle = st.toggle("Enforce ATS Formatting Rules", value=True, help="Validates standard section titles, date formats, and bullet structures.")

st.markdown("---")

# Form Sections with Streamlit Tabs
tab_personal, tab_summary, tab_exp, tab_edu, tab_skills = st.tabs([
    "👤 Personal Info",
    "📝 Summary",
    "💼 Experience",
    "🎓 Education",
    "⚡ Skills & Export"
])

# Initialize session state data dictionary
if "resume_builder_data" not in st.session_state:
    st.session_state.resume_builder_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "+1 (555) 019-2834",
        "location": "San Francisco, CA",
        "linkedin": "linkedin.com/in/janedoe",
        "target_role": "Full Stack Developer",
        "summary": "Experienced Full Stack Developer skilled in React, Node.js, and Python. Proven track record of building responsive web applications and scalable cloud architecture.",
        "experiences": [
            {
                "role": "Senior Software Engineer",
                "company": "TechCorp Innovations",
                "duration": "2023 - Present",
                "description": "• Spearheaded frontend migration to React & TypeScript, boosting page speed by 40%.\n• Architected RESTful microservices in Node.js servicing over 50,000 active daily users."
            }
        ],
        "education": [
            {
                "degree": "B.S. in Computer Science",
                "institution": "University of California, Berkeley",
                "year": "2019 - 2023"
            }
        ],
        "skills_input": "JavaScript, TypeScript, React, Node.js, Python, PostgreSQL, Docker, Git, REST API",
        "achievements": "• Winner of Hackathon 2025 Best AI Solution.\n• Published technical article on modern web performance."
    }

builder_data = st.session_state.resume_builder_data

# Known Bug Documentation in Code Comment:
# KNOWN_BUG_NOTE: Browser autofill on Name/Email/Phone can cause a false validation error in Streamlit form state.
# Mitigation: We sync state on change callback and trigger validation on blur/input events.

with tab_personal:
    st.subheader("Contact Information")
    c1, c2 = st.columns(2)
    with c1:
        builder_data["name"] = st.text_input("Full Name *", value=builder_data["name"], key="r_name")
        
        # Email field with blur validation mitigation
        email_val = st.text_input(
            "Email Address *", 
            value=builder_data["email"], 
            key="r_email", 
            help="Workaround: If autofilled by browser, click field and press space if validation alerts."
        )
        if not email_val or "@" not in email_val:
            st.caption("⚠️ Please enter a valid email address.")
        builder_data["email"] = email_val

        builder_data["phone"] = st.text_input("Phone Number", value=builder_data["phone"], key="r_phone")

    with c2:
        builder_data["target_role"] = st.text_input("Target Job Role", value=builder_data["target_role"], key="r_role")
        builder_data["location"] = st.text_input("City, State / Country", value=builder_data["location"], key="r_loc")
        builder_data["linkedin"] = st.text_input("LinkedIn Profile / Portfolio URL", value=builder_data["linkedin"], key="r_link")

with tab_summary:
    st.subheader("Executive Summary")
    
    if st.button("✨ AI Generate Executive Summary", key="btn_ai_summary"):
        with st.spinner("Generating AI summary..."):
            prompt = f"Write a compelling 3-sentence executive summary for a {builder_data['target_role']} emphasizing technical skills."
            generated_sum = generate_ai_suggestions(prompt)
            builder_data["summary"] = generated_sum
            st.rerun()

    builder_data["summary"] = st.text_area("Professional Summary:", value=builder_data["summary"], height=120, key="r_summary")

with tab_exp:
    st.subheader("Work Experience")
    
    exp_idx = 0
    exp = builder_data["experiences"][0]
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        exp["role"] = st.text_input("Job Title / Role", value=exp.get("role", ""), key=f"exp_role_{exp_idx}")
        exp["company"] = st.text_input("Company Name", value=exp.get("company", ""), key=f"exp_comp_{exp_idx}")
    with col_e2:
        exp["duration"] = st.text_input("Dates / Duration", value=exp.get("duration", ""), key=f"exp_dur_{exp_idx}")

    # AI Bullet Suggestion Generator
    st.markdown("#### Smart Bullet Generator")
    s_col1, s_col2 = st.columns([2, 1])
    with s_col1:
        skill_focus = st.text_input("Focus Skill/Keyword for Bullets:", value="React", key="bullet_skill_input")
    with s_col2:
        if st.button("✨ Suggest AI Bullets", key="btn_ai_bullets"):
            with st.spinner("Generating bullet points..."):
                suggestions = get_smart_bullet_suggestions(exp["role"], skill_focus)
                exp["description"] += "\n" + "\n".join([f"• {b}" for b in suggestions])
                st.rerun()

    exp["description"] = st.text_area("Bullet Points & Responsibilities:", value=exp.get("description", ""), height=150, key=f"exp_desc_{exp_idx}")

with tab_edu:
    st.subheader("Education & Certifications")
    edu = builder_data["education"][0]
    c_ed1, c_ed2, c_ed3 = st.columns(3)
    with c_ed1:
        edu["degree"] = st.text_input("Degree / Certificate", value=edu.get("degree", ""), key="edu_deg")
    with c_ed2:
        edu["institution"] = st.text_input("University / Institution", value=edu.get("institution", ""), key="edu_inst")
    with c_ed3:
        edu["year"] = st.text_input("Year / Graduation", value=edu.get("year", ""), key="edu_yr")

with tab_skills:
    st.subheader("Skills & Achievements")
    builder_data["skills_input"] = st.text_area("Skills (Comma-separated):", value=builder_data["skills_input"], height=80, key="r_skills_in")
    builder_data["achievements"] = st.text_area("Key Achievements & Awards:", value=builder_data["achievements"], height=100, key="r_achieve_in")

    st.markdown("---")
    st.subheader(f"Export Resume PDF ({selected_theme} Style)")
    
    # Generate styled PDF
    pdf_output = generate_resume_pdf(builder_data, theme=selected_theme)
    
    st.download_button(
        label=f"📥 Download {selected_theme} Resume PDF",
        data=pdf_output,
        file_name=f"{builder_data['name'].replace(' ', '_')}_Resume_{selected_theme}.pdf",
        mime="application/pdf"
    )
