# Smart AI Resume Analyzer ⚡

An all-in-one Python/Streamlit web application for analyzing, optimizing, and building ATS-friendly resumes with AI-powered diagnostics and multi-theme PDF exports.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![spaCy](https://img.shields.io/badge/spaCy-en__core__web__sm-09A3D5)
![Gemini AI](https://img.shields.io/badge/Google-Gemini_API-8E44AD)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Key Features

1. **🏠 Home**: Landing page showcasing value propositions, key metrics, and quick navigation.
2. **🔍 Resume Analyzer**:
   - PDF & DOCX text parsing with `pdfplumber` and `python-docx`.
   - ATS compatibility score with an interactive Plotly visual gauge.
   - Skill gap breakdown (missing vs. present skills chart).
   - Custom Job Description (JD) matching mode.
   - Tailored course and curated video recommendations.
   - Downloadable AI-generated PDF diagnostic report (`ReportLab`).
3. **📝 Resume Builder**:
   - Multi-theme PDF export (Modern, Minimal, Professional, Creative).
   - AI bullet point generator powered by Google Gemini (with smart offline heuristic fallback).
   - ATS formatting validation and documented browser autofill handling.
4. **📊 Dashboard**: Score trends over time, target role distribution, and historic scan logs.
5. **🎯 Job Search**: LinkedIn job listings scraper with latency notifications, market skill demand charts, and featured hiring companies.
6. **💬 Feedback**: Star rating and user review forms persisted into local SQLite database.
7. **ℹ️ About**: Product documentation, architecture summary, and MIT licensing.
8. **🔐 Admin Panel**: Login-gated analytics panel for tracking app usage and user feedback.

---

## 🔐 Default Seed Admin Credentials

| Parameter | Credential |
| :--- | :--- |
| **Username / Email** | `admin@example.com` |
| **Password** | `admin123` |

---

## ⚙️ Local Setup Instructions

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/smart-resume-ai.git
cd smart-resume-ai
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables
Create a file named `utils/.env` and insert your Gemini API Key:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 5. Run Application
```bash
streamlit run app.py
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
