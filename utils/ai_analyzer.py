import json
import os
import google.generativeai as genai

class AIAnalyzer:
    def __init__(self):
        self.model = "gemini-pro"
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise Exception("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=self.api_key)
        
    def test_api_key(self):
        """Test if the API key is valid."""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content("Test.")
            return True
        except Exception as e:
            return str(e)

    def analyze_policy(self, policy_text):
        """Analyze policy text and provide recommendations."""
        try:
            model = genai.GenerativeModel(self.model)
            prompt = """
            Analyze this policy and provide insights in JSON format with the following structure:
            {
                'summary': 'Brief summary of the policy',
                'recommendations': ['List of recommendations'],
                'risk_areas': ['Potential risk areas'],
                'compliance_score': 'Score between 0 and 1'
            }

            Policy text:
            """ + policy_text

            response = model.generate_content(prompt)
            # Extract JSON from response
            json_str = response.text.strip().strip('```json').strip('```').strip()
            return json.loads(json_str)
        except Exception as e:
            raise Exception(f"Failed to analyze policy: {e}")

    def compare_policies(self, old_policy, new_policy):
        """Compare two policy versions and highlight changes."""
        try:
            model = genai.GenerativeModel(self.model)
            prompt = f"""
            Compare these two policy versions and identify key changes.
            Always include a similarity_score between 0 and 1.
            
            Respond in JSON format with:
            {{
                'similarity_score': 0.8,  # Example score
                'added': ['List of added elements'],
                'removed': ['List of removed elements'],
                'modified': ['List of modified elements'],
                'impact_analysis': 'Analysis of the changes impact'
            }}

            Old policy:
            {old_policy}

            New policy:
            {new_policy}
            """

            response = model.generate_content(prompt)
            # Extract JSON from response
            json_str = response.text.strip().strip('```json').strip('```').strip()
            return json.loads(json_str)
        except Exception as e:
            return {
                'similarity_score': 0,
                'added': [],
                'removed': [],
                'modified': [],
                'impact_analysis': f"Error comparing policies: {str(e)}"
            }

    def update_policy(self, enterprise_policy, government_policy, industry):
        """Generate updated enterprise policy based on government policy."""
        try:
            model = genai.GenerativeModel(self.model)
            prompt = f"""
            Update the enterprise policy to comply with the new government policy.
            Keep the core business requirements while ensuring compliance.
            
            Industry: {industry}
            Enterprise Policy: {enterprise_policy}
            Government Policy: {government_policy}
            
            Return only the updated policy text without any additional formatting.
            """
            
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Failed to update policy: {e}")
        try:
            model = genai.GenerativeModel(self.model)
            prompt = f"""
            Compare these two policy versions and identify key changes.
            Respond in JSON format with:
            {{
                'added': ['List of added elements'],
                'removed': ['List of removed elements'],
                'modified': ['List of modified elements'],
                'impact_analysis': 'Analysis of the changes impact'
            }}

            Old policy:
            {old_policy}

            New policy:
            {new_policy}
            """

            response = model.generate_content(prompt)
            # Extract JSON from response
            json_str = response.text.strip().strip('```json').strip('```').strip()
            return json.loads(json_str)
        except Exception as e:
            raise Exception(f"Failed to compare policies: {e}")