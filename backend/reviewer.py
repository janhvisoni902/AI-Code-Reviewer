import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def review_content(content: str, review_type: str = "general") -> str:
    """
    Sends code to Groq LLM for review and returns the markdown response.
    
    Args:
        content (str): The code to review.
        review_type (str): Optional context type (e.g. 'security', 'performance').
    
    Returns:
        str: The AI-generated review in markdown format.
    """

    # ✅ FIX 1: Use plain string with .format() only — no f-string prefix
    prompt = """
You are an expert senior software engineer and code reviewer with 15+ years of experience.

Perform a professional {review_type} code review.

Follow this EXACT markdown format strictly:

## 📊 Overall Score: X/10

## 🐛 Bugs & Errors
- List bugs or write: ✅ No bugs found.

## ⚠️ Code Quality Issues
- List readability, naming, structure issues.

## 🔒 Security Vulnerabilities
- List risks or write: ✅ No security issues found.

## ⚡ Performance Improvements
- List inefficiencies or write: None.

## 💡 Best Practice Suggestions
- Suggest improvements.

## ✅ What's Done Well
- Mention positives.

## 🔧 Refactored Code
- Provide an improved version of the code inside a code block.

Now review this code:

{code}
""".format(code=content, review_type=review_type)  # ✅ FIX 2: review_type now used

    # ✅ FIX 3: Added error handling + proper indentation
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",       # ✅ FIX 4: correct indentation
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,                     # ✅ BONUS: lower = more consistent output
            max_tokens=2048                      # ✅ BONUS: prevent truncated responses
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error during review: {str(e)}"  # ✅ FIX 5: graceful error handling