```python
import os
import requests
import streamlit as st


# ==========================================================
# SMART RX AI — META MUSE GLIMMER ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Generates an explainable safety summary using
    Meta's Muse Glimmer model through Hugging Face
    Inference Providers.

    The Hugging Face token is stored securely in
    Streamlit Secrets and is never included in
    the repository.
    """

    # ======================================================
    # LOAD HUGGING FACE TOKEN
    # ======================================================

    try:
        hf_token = st.secrets.get(
            "HF_TOKEN",
            os.getenv("HF_TOKEN")
        )
    except Exception:
        hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        return (
            "🤖 AI explanation is currently unavailable.\n\n"
            "The Hugging Face AI token was not detected. "
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # PREPARE AI PROMPT
    # ======================================================

    prompt = f"""
You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

You are given structured findings produced by the
SmartRx AI rule-based safety engine.

Explain ONLY the information contained in those findings.

Review:

1. Selected medicines.
2. Duplicate active ingredients.
3. Medicine-class or combination warnings.
4. Selected Nigerian or Traditional African medicinal herbs.
5. Herbal safety information contained in the database.
6. Any missing or uncertain information.

IMPORTANT SAFETY RULES:

- Do not diagnose the user.
- Do not prescribe medicines.
- Do not recommend starting, stopping, or changing medication.
- Do not invent drug-herb interactions.
- Do not claim an interaction exists unless supported by
  the structured findings.
- Clearly distinguish database information from uncertainty.
- If no herb-drug interaction information is provided,
  say that the available SmartRx AI database does not
  establish an interaction.
- Explain duplicate ingredients clearly.
- Explain medicine-class warnings clearly.
- Use simple language suitable for a general Nigerian audience.
- Recommend consultation with a qualified doctor or pharmacist
  when a potential safety concern is identified.

STRUCTURED SMART RX AI FINDINGS:

{safety_findings}

Use these sections:

### Overall Safety Summary

Briefly summarize the main findings.

### Medicine Findings

Explain duplicate ingredients and medicine-class warnings,
if any.

### Herbal Findings

Explain the selected herbs and their stored safety information.
Do not invent additional interactions.

### Important Safety Advice

Provide concise safety advice based only on the findings.

### Professional Guidance

State when the user should consult a qualified healthcare
professional.

Remember: SmartRx AI is an educational and decision-support
platform. It does not replace professional medical advice.
"""

    # ======================================================
    # CALL HUGGING FACE INFERENCE PROVIDER
    # ======================================================

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

        # ==================================================
        # CHECK HTTP RESPONSE
        # ==================================================

        response.raise_for_status()

        result = response.json()

        # ==================================================
        # EXTRACT AI RESPONSE
        # ==================================================

        choices = result.get("choices", [])

        if choices:

            message = choices[0].get("message", {})

            content = message.get("content", "")

            if content:
                return content

        return (
            "🤖 The AI explanation service returned an "
            "unexpected response.\n\n"
            "The structured SmartRx AI safety screening "
            "remains available."
        )

    # ======================================================
    # TIMEOUT
    # ======================================================

    except requests.exceptions.Timeout:

        return (
            "🤖 The AI explanation service timed out.\n\n"
            "Please try the safety verification again. "
            "The structured SmartRx AI safety screening "
            "remains available."
        )

    # ======================================================
    # HTTP / CONNECTION ERROR
    # ======================================================

    except requests.exceptions.RequestException as error:

        return (
            "🤖 The AI explanation service is temporarily "
            "unavailable.\n\n"
            "The structured SmartRx AI safety screening "
            "remains available."
        )

    # ======================================================
    # UNEXPECTED ERROR
    # ======================================================

    except Exception:

        return (
            "🤖 The AI explanation service encountered an "
            "unexpected error.\n\n"
            "The structured SmartRx AI safety screening "
            "remains available."
        )
```
