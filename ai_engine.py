import os
import requests


# ==========================================================
# SMART RX AI — META AI ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Sends structured SmartRx AI safety findings
    to a Meta AI-compatible inference endpoint.

    The API key is read securely from an environment
    variable and is never stored in the repository.
    """

    api_key = os.getenv("META_AI_API_KEY")

    if not api_key:
        return (
            "AI explanation is currently unavailable. "
            "The structured SmartRx safety screening has "
            "still been completed."
        )

    prompt = f"""
You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety platform.

Review the structured safety findings below.

Your task is to:
1. Explain the identified medication safety issues.
2. Explain any duplicate active ingredients.
3. Explain potential herb–drug interaction concerns.
4. Clearly distinguish confirmed database findings
   from areas where evidence is limited.
5. Provide a concise, understandable safety summary.
6. Never invent a drug interaction or medical fact.
7. Do not diagnose the user.
8. Encourage consultation with a qualified healthcare
   professional where appropriate.

Structured SmartRx AI findings:

{safety_findings}

Return a clear, professional explanation suitable
for a medication-safety application.
"""

    try:

        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-models/Muse-Glimmer-30B",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 700
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as error:

        return (
            "AI explanation could not be generated at this time.\n\n"
            f"Technical status: {error}\n\n"
            "The structured SmartRx safety screening remains available."
        )
