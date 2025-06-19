import os
import google.generativeai as genai
from dotenv import load_dotenv
import textwrap
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Configure Gemini - using current stable model
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # Using both pro and flash models with fallback
    model_pro = genai.GenerativeModel('gemini-1.5-pro-latest')
    model_flash = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    raise RuntimeError(f"Failed to configure Gemini API: {str(e)}")

def format_response(text: str) -> str:
    """Format the AI response for better readability."""
    return textwrap.fill(text, width=80)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))
def generate_with_fallback(prompt: str) -> str:
    """Try with pro model first, fallback to flash if rate limited."""
    try:
        response = model_pro.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2000
            }
        )
        return response.text
    except Exception as e:
        if "429" in str(e):  # Rate limited
            print("⚠️ Pro model rate limited, trying flash model...")
            response = model_flash.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 2000
                }
            )
            return response.text
        raise

def ai_compliance_check(policy_text: str) -> str:
    """Check policy compliance with RTI Act requirements.
    
    Args:
        policy_text: Text extracted from PDF policy document
        
    Returns:
        Formatted compliance assessment or error message
    """
    guideline = """According to RTI Act Section 4(1)(b), every public authority must proactively disclose:
    1. Organizational structure
    2. Powers and duties of officers
    3. Financial records
    4. Rules and regulations
    5. Procedures followed in decision making
    6. Mechanisms for public interaction
    7. Directory of officers and employees"""

    prompt = f"""
    You are a policy compliance expert specializing in Right to Information (RTI) regulations.

    GOVERNMENT COMPLIANCE GUIDELINES:
    {guideline}

    POLICY TO REVIEW:
    {policy_text[:4000]}  # Limiting to context window

    TASK:
    1. Assess if the policy complies with the above guidelines
    2. Identify exactly what is missing (be specific)
    3. Suggest concrete improvements
    4. Rate compliance on a scale of 1-10
    5. Provide recommendations in bullet points

    OUTPUT FORMAT:
    - Compliance Rating: [1-10]
    - Missing Elements: [list]
    - Suggested Improvements: [bulleted list]
    - Overall Assessment: [2-3 sentences]
    """

    try:
        start_time = time.time()
        response_text = generate_with_fallback(prompt)
        
        if not response_text:
            return "⚠️ Received empty response from Gemini API"
            
        processing_time = time.time() - start_time
        print(f"Processed in {processing_time:.2f} seconds")
        return format_response(response_text)
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            if "retry_delay" in error_msg:
                wait_time = int(error_msg.split("seconds: ")[1].split("}")[0])
                return f"❌ Rate limited. Please wait {wait_time} seconds and try again."
            return "❌ Rate limited. Please try again later."
        return f"❌ Gemini API Error: {error_msg}\nPlease check your API key and network connection."

if __name__ == "__main__":
    # Test with sample text
    sample_text = "This is a sample policy text about our organization..."
    print("Testing Gemini API...")
    result = ai_compliance_check(sample_text)
    print("\nResult:")
    print(result)