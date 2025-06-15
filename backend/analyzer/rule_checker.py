import re
from typing import Dict

def rule_based_analysis(text: str) -> Dict[str, str]:
    results = {}

    # Rule 1: Required sections
    required_sections = ['Purpose', 'Scope', 'Policy', 'Compliance', 'Enforcement', 'Definitions']
    for section in required_sections:
        pattern = rf'\b{section}\b'
        results[section] = "Present ✅" if re.search(pattern, text, re.IGNORECASE) else "Missing ❌"

    # Rule 2: Keywords indicating compliance
    keywords = ['GDPR', 'confidentiality', 'data retention', 'ISO 27001', 'PCI-DSS']
    for keyword in keywords:
        results[keyword] = "Found ✅" if re.search(keyword, text, re.IGNORECASE) else "Not Found ❌"

    # Rule 3: Flag outdated references
    outdated_refs = ['2011', 'ISO 27001:2005', 'IT Act 2000']
    for item in outdated_refs:
        results[f"Outdated Ref: {item}"] = "Used ⚠️" if item in text else "Not Used ✅"

    return results
