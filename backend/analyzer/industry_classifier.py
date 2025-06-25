import re

def detect_industry(text: str) -> str:
    # Simple keyword-based heuristic (can replace with AI later)
    text = text.lower()

    industry_keywords = {
        "healthcare": ["hospital", "patient", "clinical", "medical"],
        "finance": ["investment", "audit", "balance sheet", "loan", "banking"],
        "education": ["university", "students", "academic", "syllabus", "faculty"],
        "technology": ["cybersecurity", "software", "data privacy", "it act"],
        "manufacturing": ["plant", "factory", "supply chain", "production"],
        "government": ["ministry", "rti", "act", "public authority", "regulation"],
    }

    for industry, keywords in industry_keywords.items():
        if any(kw in text for kw in keywords):
            return industry.capitalize()

    return "General"
