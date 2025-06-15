import re

def clean_text(text: str) -> str:
    """
    Cleans extracted policy text by removing extra whitespace, line breaks,
    headers/footers, non-informative symbols, etc.
    """

    # Remove line breaks and excessive whitespace
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)

    # Remove page numbers or "Page x of y" patterns
    text = re.sub(r'Page\s*\d+\s*(of\s*\d+)?', '', text, flags=re.IGNORECASE)

    # Remove common special characters (can expand this list later)
    text = re.sub(r'[•●■◆►▪]', '', text)
    
    # Optionally remove digits-only lines
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)

    # Remove repeated dashes or underscores
    text = re.sub(r'[-_]{2,}', '', text)

    return text.strip()
