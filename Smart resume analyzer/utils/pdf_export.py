import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def generate_analysis_report_pdf(analysis_result: dict, filename: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    story = []

    # Title Banner Style
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor('#1E293B'),
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#64748B'),
        alignment=TA_LEFT,
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#4F46E5'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        leading=14,
        spaceAfter=6
    )

    story.append(Paragraph("Smart AI Resume Analyzer - Diagnostic Report", title_style))
    story.append(Paragraph(f"Analyzed File: <b>{filename}</b> | Target Role: <b>{analysis_result.get('target_role', 'N/A')}</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4F46E5'), spaceAfter=15))

    # ATS Score Summary Table
    score = analysis_result.get('overall_score', 0)
    score_color = colors.HexColor('#10B981') if score >= 80 else (colors.HexColor('#F59E0B') if score >= 60 else colors.HexColor('#EF4444'))

    score_data = [
        [Paragraph("<b>Overall ATS Compatibility Score</b>", body_style), Paragraph(f"<b><font size=16 color='{score_color.hexval()}'>{score}%</font></b>", body_style)],
        [Paragraph("Skill Match Score", body_style), Paragraph(f"{analysis_result.get('skill_score', 0)}%", body_style)],
        [Paragraph("Content Similarity Score", body_style), Paragraph(f"{analysis_result.get('similarity_score', 0)}%", body_style)],
        [Paragraph("Format & Structure Score", body_style), Paragraph(f"{analysis_result.get('format_score', 0)}%", body_style)]
    ]

    score_table = Table(score_data, colWidths=[280, 200])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 15))

    # Present vs Missing Skills
    story.append(Paragraph("Skills & Keyword Gap Analysis", h2_style))
    present = ", ".join(analysis_result.get('present_skills', [])) or "None identified"
    missing = ", ".join(analysis_result.get('missing_skills', [])) or "None (Full match!)"

    skills_data = [
        [Paragraph("<b>Matched Skills</b>", body_style), Paragraph(f"<font color='#10B981'>{present}</font>", body_style)],
        [Paragraph("<b>Missing / Gap Skills</b>", body_style), Paragraph(f"<font color='#EF4444'>{missing}</font>", body_style)]
    ]

    skills_table = Table(skills_data, colWidths=[150, 330])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 15))

    # Recommendations
    story.append(Paragraph("Recommended Action Items", h2_style))
    recs = [
        "Incorporate missing target keywords into your work experience bullet points.",
        "Quantify your accomplishments using specific metrics, revenue growth, or % optimization.",
        "Keep resume formatting clean with standard fonts and consistent section headings.",
        "Review target course recommendations to bridge identified technical skill gaps."
    ]
    for r in recs:
        story.append(Paragraph(f"• {r}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_resume_pdf(data: dict, theme: str = "Modern") -> bytes:
    """Generates styled Resume PDF based on selected theme: Modern, Minimal, Professional, Creative."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    story = []

    # Theme Theme Palette Mapping
    theme_colors = {
        "Modern": {"primary": "#4F46E5", "secondary": "#1E293B", "text": "#334155", "bar": "#E0E7FF"},
        "Minimal": {"primary": "#0F172A", "secondary": "#475569", "text": "#334155", "bar": "#94A3B8"},
        "Professional": {"primary": "#1E3A8A", "secondary": "#1E293B", "text": "#334155", "bar": "#DBEAFE"},
        "Creative": {"primary": "#0D9488", "secondary": "#0F766E", "text": "#334155", "bar": "#CCFBF1"}
    }
    palette = theme_colors.get(theme, theme_colors["Modern"])

    name_style = ParagraphStyle(
        'RName',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24 if theme != "Minimal" else 20,
        textColor=colors.HexColor(palette['primary']),
        alignment=TA_CENTER if theme in ["Modern", "Creative"] else TA_LEFT,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'RContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor(palette['secondary']),
        alignment=TA_CENTER if theme in ["Modern", "Creative"] else TA_LEFT,
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'RSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor(palette['primary']),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'RBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=colors.HexColor(palette['text']),
        leading=13.5,
        spaceAfter=4
    )

    # Header
    name = data.get("name", "John Doe")
    email = data.get("email", "john@example.com")
    phone = data.get("phone", "+1 234 567 890")
    location = data.get("location", "New York, NY")
    linkedin = data.get("linkedin", "linkedin.com/in/johndoe")
    title = data.get("target_role", "Software Engineer")

    story.append(Paragraph(f"<b>{name.upper()}</b>", name_style))
    contact_line = f"{title} | {email} | {phone} | {location} | {linkedin}"
    story.append(Paragraph(contact_line, contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor(palette['primary']), spaceAfter=10))

    # Executive Summary
    if data.get("summary"):
        story.append(Paragraph("EXECUTIVE SUMMARY", section_heading))
        story.append(Paragraph(data["summary"], body_style))
        story.append(Spacer(1, 6))

    # Work Experience
    experiences = data.get("experiences", [])
    if experiences:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
        for exp in experiences:
            comp_role = f"<b>{exp.get('role', 'Position')}</b> - {exp.get('company', 'Company')} ({exp.get('duration', '2023 - Present')})"
            story.append(Paragraph(comp_role, body_style))
            desc = exp.get("description", "")
            if desc:
                for line in desc.split("\n"):
                    if line.strip():
                        bullet = line.strip("•- ")
                        story.append(Paragraph(f"• {bullet}", body_style))
            story.append(Spacer(1, 4))

    # Education
    education = data.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", section_heading))
        for edu in education:
            edu_line = f"<b>{edu.get('degree', 'Degree')}</b> - {edu.get('institution', 'University')} ({edu.get('year', '2022')})"
            story.append(Paragraph(edu_line, body_style))
        story.append(Spacer(1, 6))

    # Skills & Achievements
    skills_str = data.get("skills_input", "")
    if skills_str:
        story.append(Paragraph("SKILLS & COMPETENCIES", section_heading))
        story.append(Paragraph(skills_str, body_style))
        story.append(Spacer(1, 6))

    achievements = data.get("achievements", "")
    if achievements:
        story.append(Paragraph("KEY ACHIEVEMENTS", section_heading))
        for item in achievements.split("\n"):
            if item.strip():
                story.append(Paragraph(f"• {item.strip('•- ')}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
