from typing import Dict
from backend.services.gemini import GeminiService
from backend.analyzer.rule_checker import rule_based_analysis

class PolicyComparator:
    def __init__(self):
        self.gemini = GeminiService()
    
    def compare_with_government(self, policy_text: str, gov_policy_text: str) -> Dict:
        # Rule-based comparison
        rule_results = rule_based_analysis(policy_text, gov_policy_text)
        
        # AI comparison
        prompt = f"""Compare these policies and identify gaps:
        Enterprise Policy:
        {policy_text}
        
        Government Standard:
        {gov_policy_text}"""
        
        ai_results = self.gemini.generate(prompt)
        
        return {
            "rule_based": rule_results,
            "ai_analysis": ai_results,
            "compliance_score": self._calculate_score(rule_results, ai_results)
        }
    
    def _calculate_score(self, rule_results, ai_results):
        # Simplified scoring (to be enhanced based on actual logic)
        rule_score = sum(1 for v in rule_results.values() if "✅" in v) / len(rule_results) * 50
        ai_score = 50 if "compliant" in ai_results.lower() else 0
        return min(rule_score + ai_score, 100)