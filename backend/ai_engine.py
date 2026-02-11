import os

KB_PATH = "knowledge_base"

# Role keyword → knowledge file mapping
ROLE_FILE_MAP = {
    # Software roles
    "software developer": "software_developer.txt",
    "software development": "software_developer.txt",
    "developer": "software_developer.txt",
    "programmer": "software_developer.txt",
    "coding": "software_developer.txt",

    # Data roles
    "data analyst": "data_analyst.txt",
    "data analysis": "data_analyst.txt",
    "data scientist": "data_scientist.txt",

    # AI roles
    "ai engineer": "ai_ml_engineer.txt",
    "ml engineer": "ai_ml_engineer.txt",
    "machine learning": "ai_ml_engineer.txt",

    # Security
    "cybersecurity": "cybersecurity.txt",
    "security": "cybersecurity.txt",

    # Design
    "designer": "ui_ux_designer.txt",
    "ui/ux": "ui_ux_designer.txt",
    "ui": "ui_ux_designer.txt",
    "ux": "ui_ux_designer.txt",

    # Business
    "marketing": "digital_marketing.txt",
    "digital marketing": "digital_marketing.txt",

    "accountant": "accountant.txt",
    "accounting": "accountant.txt"
}

CAREER_KEYWORDS = [
    "job", "career", "future", "skills", "ai", "automation",
    "developer", "development", "engineer", "analyst",
    "designer", "accountant"
]


def is_career_related(question: str) -> bool:
    q = question.lower()
    return any(keyword in q for keyword in CAREER_KEYWORDS)


def get_relevant_files(question: str):
    q = question.lower()
    matched_files = set()

    for keyword, file in ROLE_FILE_MAP.items():
        if keyword in q:
            matched_files.add(file)

    return list(matched_files)


def answer_question_with_knowledge(question, history=None):
    if not question or len(question.strip()) < 5:
        return {
            "answer": "Please ask a clear and specific question about careers or jobs.",
            "sources": []
        }

    if not is_career_related(question):
        return {
            "answer": (
                "I focus on career-related questions and how AI may impact jobs.\n\n"
                "Examples you can ask:\n"
                "- Is software development a future safe career?\n"
                "- Will AI replace accountants?\n"
                "- What skills should students learn in the AI era?"
            ),
            "sources": []
        }

    relevant_files = get_relevant_files(question)

    context = ""
    sources = []

    if not relevant_files:
        return {
            "answer": (
                "I couldn't identify a specific role from your question.\n\n"
                "However, in general, careers involving creativity, problem-solving, "
                "decision-making, and domain expertise are more resilient to AI automation."
            ),
            "sources": []
        }

    for file in relevant_files:
        file_path = os.path.join(KB_PATH, file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                context += f"\n--- {file} ---\n"
                context += f.read()
                sources.append(file)

    answer = f"""
Based on role-specific career data, here is the analysis:

{context}

User Question:
{question}

Conclusion:
AI will automate repetitive tasks in this role, but professionals who focus on
higher-level thinking, system design, creativity, and collaboration with AI
tools will remain valuable in the future job market.
"""

    return {
        "answer": answer.strip(),
        "sources": sources
    }