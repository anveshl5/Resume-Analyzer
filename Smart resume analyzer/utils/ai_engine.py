import os
from dotenv import load_dotenv

# Load env variables from utils/.env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Configure Gemini if available
gemini_model = None
if GEMINI_API_KEY and GEMINI_API_KEY != "your_google_gemini_api_key":
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        # Use available model
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Gemini initialization error: {e}")
        gemini_model = None

def generate_ai_suggestions(prompt: str) -> str:
    """Invokes Gemini API or falls back to offline AI heuristics engine."""
    if gemini_model:
        try:
            response = gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Gemini API call failed: {e}. Switching to offline engine.")
            
    # Intelligent offline fallback response
    return generate_offline_fallback(prompt)

def generate_offline_fallback(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "bullet point" in prompt_lower or "achievement" in prompt_lower:
        return (
            "• Spearheaded cross-functional team initiatives to optimize workflow efficiency, boosting productivity by 28%.\n"
            "• Developed and deployed scalable microservices architectures using Python, Docker, and CI/CD pipelines.\n"
            "• Reduced system latency by 35% through query optimization and implementing Redis caching strategies.\n"
            "• Collaborated with product managers and stakeholders to align technical deliverables with key business metrics."
        )
    elif "summary" in prompt_lower:
        return (
            "Results-driven technology professional with extensive hands-on experience designing, developing, and executing high-impact solutions. "
            "Adept in leveraging modern analytical tools, clean software architecture, and collaborative agile methodologies to solve complex engineering challenges."
        )
    elif "feedback" in prompt_lower or "recommendation" in prompt_lower:
        return (
            "1. **Quantify Achievements**: Ensure every experience section includes metrics (e.g. '% increase', '$ cost saved', 'X users reached').\n"
            "2. **Keyword Optimization**: Integrate core technical skills directly into job experience descriptions rather than isolating them in a skills section.\n"
            "3. **Action Verbs**: Begin bullet points with strong verbs (e.g., 'Spearheaded', 'Engineered', 'Optimized', 'Architected')."
        )
    else:
        return (
            "• Formulated data-driven strategies that accelerated product adoption across enterprise clients.\n"
            "• Streamlined code review processes, decreasing pull request lead time by 40%.\n"
            "• Mentored junior engineers and conducted technical workshops on best development practices."
        )

def get_smart_bullet_suggestions(role: str, skill: str) -> list:
    prompt = f"Generate 3 impressive, ATS-friendly action bullet points for a {role} experienced in {skill}."
    raw = generate_ai_suggestions(prompt)
    lines = [line.strip("•- 123456789.") for line in raw.split("\n") if line.strip()]
    return lines[:3] if lines else [
        f"Engineered high-performance solutions using {skill} tailored for {role} deliverables.",
        f"Optimized system reliability and operational efficiency leveraging {skill}.",
        f"Collaborated with cross-functional teams to integrate {skill} best practices."
    ]

def get_role_insights(role: str) -> str:
    prompt = f"Provide 3 high-level industry trends and key demands for the role of {role} in 2026."
    return generate_ai_suggestions(prompt)
