import re
from typing import Dict, List, Any

def clean_text(text):
    if not text:
        return text
    # Join broken lines
    text = re.sub(r'([a-z,])\n([a-z])', r'\1 \2', text, flags=re.IGNORECASE)
    # Standardize bullet points
    text = re.sub(r'\n\s*[*\-•]', '\n•', text)
    # Clean up spaces
    text = ' '.join(text.split())
    return text

def parse_ai_review(ai_text: str) -> Dict[str, Any]:
    if not ai_text:
        return {
            "compliance_score": None,
            "missing": [],
            "suggestions": [],
            "raw": ""
        }

    compliance_score = None
    missing = []
    suggestions = []

    # Extract Compliance Rating
    score_match = re.search(r"\*\*Compliance Rating:\*\*\s*(\d+)/10", ai_text)
    if score_match:
        compliance_score = int(score_match.group(1))

    # Extract Missing Elements Block
    missing_block = ""
    suggestions_block = ""

    missing_match = re.search(r"\*\*Missing Elements:\*\*(.*?)(\*\*Suggested Improvements:\*\*|$)", ai_text, re.DOTALL)
    if missing_match:
        missing_block = missing_match.group(1)

    suggestions_match = re.search(r"\*\*Suggested Improvements:\*\*(.*?)(\*\*Overall Assessment:\*\*|$)", ai_text, re.DOTALL)
    if suggestions_match:
        suggestions_block = suggestions_match.group(1)

    # Clean bullet list from blocks
    missing = re.findall(r"(?:[*\-•])\s*(.*?)\s*(?=\n(?:[*\-•])|$)", missing_block.strip(), re.DOTALL)
    suggestions = re.findall(r"(?:[*\-•])\s*(.*?)\s*(?=\n(?:[*\-•])|$)", suggestions_block.strip(), re.DOTALL)

    # Final cleanup
    missing = [clean_text(m.strip()) for m in missing if m.strip()]
    suggestions = [clean_text(s.strip()) for s in suggestions if s.strip()]


    return {
        "compliance_score": compliance_score,
        "missing": missing,
        "suggestions": suggestions,
        "raw": ai_text.strip()
    }
