import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Target Role predefined required skill maps
ROLE_SKILL_MAP = {
    "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "SQL", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "Data Visualization", "R"],
    "Full Stack Developer": ["JavaScript", "TypeScript", "React", "Node.js", "Python", "HTML", "CSS", "SQL", "Git", "REST API", "Docker", "MongoDB"],
    "Frontend Engineer": ["JavaScript", "TypeScript", "React", "Vue.js", "HTML", "CSS", "Tailwind CSS", "Redux", "REST API", "Git"],
    "Backend Engineer": ["Python", "Java", "Node.js", "Go", "Django", "FastAPI", "SQL", "PostgreSQL", "Redis", "Docker", "Kubernetes", "REST API"],
    "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "Linux", "Bash", "CI/CD", "Git", "Python", "Terraform", "Azure", "GCP"],
    "AI / ML Engineer": ["Python", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Machine Learning", "Deep Learning", "Gemini API", "FastAPI", "Docker"],
    "Product Manager": ["Agile", "Scrum", "Project Management", "Data Analysis", "Leadership", "Communication", "Problem Solving", "Jira", "Strategy"]
}

# Role-based Course Recommendations
COURSE_RECOMMENDATIONS = {
    "Data Scientist": [
        {"title": "Machine Learning A-Z", "provider": "Coursera / Stanford", "url": "https://www.coursera.org/learn/machine-learning"},
        {"title": "Python for Data Science and Machine Learning Bootcamp", "provider": "Udemy", "url": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/"},
        {"title": "Deep Learning Specialization", "provider": "DeepLearning.AI", "url": "https://www.coursera.org/specializations/deep-learning"}
    ],
    "Full Stack Developer": [
        {"title": "The Complete 2026 Web Development Bootcamp", "provider": "Udemy", "url": "https://www.udemy.com/course/the-complete-web-development-bootcamp/"},
        {"title": "Full Stack Open (React, Redux, Node.js)", "provider": "University of Helsinki", "url": "https://fullstackopen.com/en/"},
        {"title": "Meta Front-End & Back-End Developer Professional Certificate", "provider": "Coursera", "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer"}
    ],
    "Frontend Engineer": [
        {"title": "Advanced React & Redux", "provider": "Frontend Masters", "url": "https://frontendmasters.com/courses/advanced-react/"},
        {"title": "CSS for JS Developers", "provider": "Josh Comeau", "url": "https://css-for-js.dev/"}
    ],
    "Backend Engineer": [
        {"title": "Backend Engineering Masterclass", "provider": "Udemy", "url": "https://www.udemy.com/course/backend-engineering-masterclass/"},
        {"title": "Distributed Systems & Microservices", "provider": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/"}
    ],
    "DevOps Engineer": [
        {"title": "Docker and Kubernetes: The Complete Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/"},
        {"title": "AWS Certified Solutions Architect", "provider": "A Cloud Guru", "url": "https://acloudguru.com/"}
    ],
    "AI / ML Engineer": [
        {"title": "Generative AI with Large Language Models", "provider": "DeepLearning.AI", "url": "https://www.coursera.org/learn/generative-ai-with-llms"},
        {"title": "Natural Language Processing Specialization", "provider": "Coursera", "url": "https://www.coursera.org/specializations/natural-language-processing"}
    ],
    "Product Manager": [
        {"title": "Become a Product Manager", "provider": "Udemy", "url": "https://www.udemy.com/course/become-a-product-manager-learn-the-skills-get-a-job/"},
        {"title": "Product Strategy", "provider": "Kellogg Executive Education", "url": "https://www.coursera.org/"}
    ]
}

# Recommended Video Links
VIDEO_RECOMMENDATIONS = {
    "Data Scientist": [
        {"title": "How I Would Learn Data Science in 2026", "channel": "Ken Jee", "url": "https://www.youtube.com/results?search_query=ken+jee+learn+data+science"},
        {"title": "Data Science Resume Review & ATS Tips", "channel": "Luke Barousse", "url": "https://www.youtube.com/results?search_query=luke+barousse+data+science+resume"}
    ],
    "Full Stack Developer": [
        {"title": "Web Development In 2026 - A Practical Guide", "channel": "Traversy Media", "url": "https://www.youtube.com/results?search_query=traversy+media+web+development+guide"},
        {"title": "10 Resume Mistakes Software Engineers Make", "channel": "Fireship", "url": "https://www.youtube.com/results?search_query=fireship+software+engineer+resume"}
    ],
    "AI / ML Engineer": [
        {"title": "Generative AI & LLM Roadmap for Engineers", "channel": "CampusX", "url": "https://www.youtube.com/results?search_query=generative+ai+roadmap"},
        {"title": "Machine Learning Interview & Resume Guide", "channel": "Krish Naik", "url": "https://www.youtube.com/results?search_query=krish+naik+ml+resume"}
    ]
}

def compute_ats_score(parsed_resume: dict, target_role: str, custom_jd: str = "") -> dict:
    resume_text = parsed_resume.get("raw_text", "")
    resume_skills = set(parsed_resume.get("skills", []))

    if custom_jd and custom_jd.strip():
        # Extract skills from custom JD
        jd_words = re.findall(r'\b[A-Za-z0-9+#.-]+\b', custom_jd)
        required_skills = list(set([w for w in jd_words if len(w) > 2]))
        # Use TF-IDF cosine similarity for text match score
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf = vectorizer.fit_transform([resume_text, custom_jd])
            similarity = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]) * 100
        except Exception:
            similarity = 65.0
        target_skill_list = [s for s in ROLE_SKILL_MAP.get(target_role, []) if s.lower() in custom_jd.lower()]
        if not target_skill_list:
            target_skill_list = ROLE_SKILL_MAP.get(target_role, ROLE_SKILL_MAP["Full Stack Developer"])
    else:
        target_skill_list = ROLE_SKILL_MAP.get(target_role, ROLE_SKILL_MAP["Full Stack Developer"])
        similarity = 70.0

    present_skills = [s for s in target_skill_list if any(s.lower() == rs.lower() or s.lower() in rs.lower() for rs in resume_skills)]
    missing_skills = [s for s in target_skill_list if s not in present_skills]

    skill_score = (len(present_skills) / len(target_skill_list)) * 100 if target_skill_list else 50.0

    # Section formatting checks
    has_email = parsed_resume.get("email") != "Not Found"
    has_phone = parsed_resume.get("phone") != "Not Found"
    word_count = parsed_resume.get("word_count", 0)
    length_score = 100.0 if 300 <= word_count <= 1200 else (70.0 if word_count > 100 else 40.0)

    format_score = 30.0 + (35.0 if has_email else 0.0) + (35.0 if has_phone else 0.0)

    # Weighted overall ATS score
    overall_score = round((skill_score * 0.50) + (similarity * 0.30) + (format_score * 0.10) + (length_score * 0.10), 1)
    overall_score = min(max(overall_score, 10.0), 99.0)

    return {
        "overall_score": overall_score,
        "skill_score": round(skill_score, 1),
        "similarity_score": round(similarity, 1),
        "format_score": round(format_score, 1),
        "target_role": target_role,
        "present_skills": present_skills,
        "missing_skills": missing_skills,
        "courses": COURSE_RECOMMENDATIONS.get(target_role, COURSE_RECOMMENDATIONS["Full Stack Developer"]),
        "videos": VIDEO_RECOMMENDATIONS.get(target_role, VIDEO_RECOMMENDATIONS["Full Stack Developer"])
    }

def get_highlighted_text(text: str, keywords: list) -> str:
    """Returns HTML with highlighted keywords."""
    highlighted = text
    for kw in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
        highlighted = pattern.sub(r'<span class="highlight-kw">\1</span>', highlighted)
    return highlighted
