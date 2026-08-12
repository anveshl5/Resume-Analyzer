# Resume-Analyzer
AI-powered Resume Analyzer that parses resumes, matches them against job descriptions using NLP/keyword analysis, and gives ATS-friendliness scores with actionable feedback. Built with FastAPI + React.
# Resume-Analyzer

AI-powered **Resume Analyzer** that parses resumes, matches them against job descriptions using NLP and keyword analysis, and provides an **ATS-friendliness score with actionable feedback**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

* 📤 Upload resumes in **PDF/DOCX** format
* 🧠 Automatically parse resumes into structured sections:

  * Contact Information
  * Skills
  * Experience
  * Education
  * Projects
* 🎯 Match resume content against a pasted **Job Description**
* 📊 Generate an **ATS-friendliness score (0–100)**
* 📈 Provide a detailed scoring breakdown
* 💡 Give actionable suggestions:

  * Missing keywords
  * Weak bullet points
  * Formatting issues
  * Missing skills
* 🗂️ Optional history of previous analyses using SQLite

---

## 🛠️ Tech Stack

| Layer          | Technology                  |
| -------------- | --------------------------- |
| Frontend       | React, Tailwind CSS         |
| Backend        | Python, FastAPI             |
| Resume Parsing | pdfplumber, python-docx     |
| NLP / Matching | spaCy, scikit-learn, TF-IDF |
| Database       | SQLite                      |
| Testing        | Pytest                      |

---

## 📁 Project Structure

```text
Resume-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── parser/              # Resume parsing logic
│   │   ├── scoring/             # ATS scoring & keyword matching
│   │   ├── models/              # Database models
│   │   └── api/                 # API route handlers
│   │
│   └── tests/                   # Pytest test suite
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   │
│   └── package.json
│
├── README.md
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.10+
* Node.js 18+
* npm or yarn

### Backend Setup

```bash
cd backend

python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

**http://localhost:8000**

FastAPI documentation:

**http://localhost:8000/docs**

---

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

**http://localhost:5173**

---

## 🧪 Running Tests

Run the backend tests using:

```bash
cd backend
pytest tests/ -v
```

---

## 📸 Screenshots

Add screenshots of your application once the UI is ready.

| Upload Screen                                | Analysis Dashboard                                   |
| -------------------------------------------- | ---------------------------------------------------- |
| ![Upload Screen](docs/screenshot-upload.png) | ![Analysis Dashboard](docs/screenshot-dashboard.png) |

---

## 🧠 How It Works

The Resume Analyzer follows these steps:

```text
Resume Upload
      ↓
PDF / DOCX Text Extraction
      ↓
Resume Section Parsing
      ↓
Job Description Analysis
      ↓
Keyword & Skill Matching
      ↓
TF-IDF / NLP Analysis
      ↓
ATS Score Calculation
      ↓
Detailed Feedback & Suggestions
```

### ATS Score

The application evaluates factors such as:

* Keyword matching
* Required skills
* Relevant experience
* Education
* Projects
* Resume structure
* Formatting
* Job-description relevance

The final score is calculated on a scale of **0–100**.

---

## 🗺️ Roadmap

* [x] Resume parsing — PDF/DOCX
* [x] Resume section extraction
* [x] Keyword matching
* [x] TF-IDF matching engine
* [x] ATS scoring algorithm
* [ ] React dashboard UI
* [ ] Analysis history using SQLite
* [ ] User authentication
* [ ] AI-powered resume improvement suggestions
* [ ] Deploy live demo
* [ ] Cloud deployment

---

## 🤝 Contributing

This is currently a solo learning project, but suggestions and contributions are welcome.

If you find a bug or have an idea for improvement:

1. Open an issue
2. Fork the repository
3. Create a new branch
4. Make your changes
5. Submit a pull request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**

* GitHub: [@yourusername](https://github.com/yourusername)
* LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

⭐ **If you find this project useful, consider giving it a star!**
vvvv
