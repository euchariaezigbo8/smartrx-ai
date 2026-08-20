import os
import requests


# ==========================================================
# SMART RX AI — META MUSE GLIMMER ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Sends structured SmartRx AI safety findings
    to Meta's Muse Glimmer model through
    Hugging Face Inference Providers.

    The Hugging Face token is stored securely
    and is never placed inside the repository.
    """

    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        return (
            "🤖 AI explanation is currently unavailable.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    prompt = f"""
You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety platform.

Review the structured safety findings below.

Your responsibilities are to:

1. Explain the identified medication safety issues.
2. Explain any duplicate active ingredients.
3. Explain potential herb–drug interaction concerns.
4. Clearly distinguish database findings from uncertainty.
5. Provide a concise and understandable safety summary.
6. Never invent a drug interaction or medical fact.
7. Do not diagnose the user.
8. Recommend consultation with a qualified healthcare
   professional when appropriate.

STRUCTURED SMARTRX AI FINDINGS:

{safety_findings}

Return a clear, professional explanation suitable
for a medication-safety application.
"""

    try:

        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {hf_token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-models/Muse-Glimmer-30B:together",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 700
            },
            timeout=90
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception:
        return (
            "🤖 The AI explanation service is temporarily "
            "unavailable.\n\n"
            "The structured SmartRx AI safety screening "
            "remains available."
        )
