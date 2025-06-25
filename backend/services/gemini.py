from backend.analyzer.gemini_checker import generate_with_fallback

class GeminiService:
    def generate(self, prompt):
        return generate_with_fallback(prompt)