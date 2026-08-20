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
a Nigerian medication and herbal safety intelligence platform.

You are given structured findings produced by SmartRx AI's
rule-based safety engine.

Your task is to explain ONLY the information contained in
the structured findings.

Review the following areas:

1. Selected orthodox medicines.
2. Duplicate active ingredients.
3. Medicine-class or combination warnings.
4. Selected Nigerian or Traditional African medicinal herbs.
5. Herbal safety information stored in the SmartRx AI knowledge base.
6. Any uncertainty or missing information.

IMPORTANT SAFETY RULES:

- Do not diagnose the user.
- Do not prescribe medicines.
- Do not recommend starting, stopping, or changing medication.
- Do not invent drug-herb interactions.
- Do not claim an interaction exists unless it is supported
  by the structured findings.
- Clearly distinguish database information from uncertainty.
- If no herb-drug interaction information is provided,
  explicitly say that the available database does not establish
  an interaction rather than guessing.
- Explain duplicate ingredients clearly when present.
- Explain medicine-class warnings clearly when present.
- Use simple language suitable for a general Nigerian audience.
- Recommend consultation with a qualified doctor or pharmacist
  when a potential safety concern is identified.

STRUCTURED SMARTRX AI FINDINGS:

{safety_findings}

Provide the response using these sections:

### Overall Safety Summary

Briefly summarize the main findings.

### Medicine Findings

Explain duplicate ingredients and medicine-class warnings,
if any.

### Herbal Findings

Explain the selected herbs and their stored safety information.
Do not invent additional interactions.

### Important Safety Advice

Provide concise, general safety advice based only on the findings.

### Professional Guidance

State when the user should consult a qualified healthcare
professional.

Remember: SmartRx AI is a decision-support and educational
platform. It does not replace professional medical advice.
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
