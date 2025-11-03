# src/ai_advisor.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from collector import load_history

# Load environment variables
load_dotenv()

# Get API key safely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "❌ OPENAI_API_KEY not found. Please create a .env file in the project root with:\n"
        "OPENAI_API_KEY=sk-proj-yourkeyhere"
    )

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def generate_ai_report(history_limit=20):
    """Generate AI-based analysis of system metrics history using GPT-4o-mini."""
    history = load_history(limit=history_limit)
    if not history:
        return "No history data available for AI analysis."

    # Prepare summary of recent metrics
    summary = "\n".join([
        f"Time: {h['timestamp']}, CPU: {h['cpu_percent']}%, "
        f"Memory: {h['memory']['percent']}%, Disk: {h['disk']['percent']}%"
        for h in history
    ])

    # Prompt for GPT-4o-mini
    prompt = f"""
    You are an AI system performance analyst. Analyze the following system metrics over time and provide:
    - Key observations
    - Detected performance issues
    - Optimizations or recommendations

    Data:
    {summary}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 🔒 always use GPT-4o-mini
            messages=[
                {"role": "system", "content": "You are a helpful performance optimization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[ERROR] AI analysis failed: {str(e)}"
