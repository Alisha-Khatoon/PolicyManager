def classify_policy_type(text: str) -> str:
    text_lower = text.lower()
    if "leave policy" in text_lower or "employee benefits" in text_lower:
        return "HR"
    elif "balance sheet" in text_lower or "financial disclosure" in text_lower:
        return "Finance"
    elif "password" in text_lower or "data protection" in text_lower:
        return "Security"
    elif "environmental" in text_lower or "sustainability" in text_lower:
        return "Environmental"
    elif "vendor" in text_lower or "procurement" in text_lower:
        return "Procurement"
    return "General"
