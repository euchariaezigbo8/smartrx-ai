import os
import requests
import streamlit as st


# ==========================================================
# SMART RX AI — AI EXPLANATION ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Generates an explainable medication and herbal
    safety summary using Meta Llama through
    Hugging Face Inference Providers.
    """

    # ======================================================
    # GET HUGGING FACE TOKEN
    # ======================================================

    try:
        hf_token = st.secrets.get("HF_TOKEN")
    except Exception:
        hf_token = None

    if not hf_token:
        hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        return (
            "🤖 Meta AI is currently unavailable.\n\n"
            "The Hugging Face API token was not detected. "
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # AI PROMPT
    # ======================================================

    prompt = f"""
You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

You are given structured findings produced by the
SmartRx AI rule-based safety engine.

Explain ONLY the information contained in those findings.

STRUCTURED SMART RX AI FINDINGS:

{safety_findings}

IMPORTANT SAFETY RULES:

- Do not diagnose the user.
- Do not prescribe medicines.
- Do not tell the user to start, stop, or change medication.
- Do not invent medicine-herb interactions.
- Do not invent herbal benefits or medical claims.
- Explain only the information contained in the findings.
- Clearly explain duplicate active ingredients.
- NEVER assign a duplicate ingredient to a specific medicine
  unless that relationship is explicitly provided in the findings.
- Do not guess which medicine contains a duplicate ingredient.
- Clearly explain medicine-class warnings.
- Keep duplicate-ingredient findings separate from
  medicine-class warnings.
- Do not transfer a warning from one finding to another.
- Only associate stomach irritation and bleeding warnings
  with NSAID combination warnings when explicitly provided.
- Explain the scientific names of selected herbs.
- Explain the traditional Nigerian names of selected herbs.
- Explain the safety cautions stored in the SmartRx database.
- Do not create additional herb-drug interactions.
- If a specific herb-drug interaction is not established
  by the supplied findings, clearly say so.
- Use simple language suitable for a general Nigerian audience.
- Recommend consultation with a qualified doctor or pharmacist
  when a safety concern is identified.

Use exactly these sections:

### Overall Safety Summary

Briefly summarize the main findings.

### Medicine Findings

Explain the selected medicines, duplicate ingredients,
and medicine-class warnings.

### Herbal Findings

Explain the selected herbs, their scientific names,
traditional Nigerian names, and safety cautions.

### Important Safety Advice

Give concise safety advice based ONLY on the supplied findings.

### Professional Guidance

Explain when the user should consult a qualified doctor
or pharmacist.

Remember that SmartRx AI is an educational and
decision-support platform. It does not replace professional
medical advice.
"""

    # ======================================================
    # SEND REQUEST TO HUGGING FACE
    # ======================================================

    try:

        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {hf_token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/Llama-3.1-8B-Instruct",
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
        # CHECK API RESPONSE
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
            "🤖 Meta AI returned an unexpected response.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # TIMEOUT
    # ======================================================

    except requests.exceptions.Timeout:

        return (
            "🤖 Meta AI took too long to respond.\n\n"
            "Please try the safety verification again. "
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # API / CONNECTION ERROR
    # ======================================================

    except requests.exceptions.RequestException as error:

        return (
            "🤖 Meta AI is temporarily unavailable.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # OTHER ERROR
    # ======================================================

    except Exception:

        return (
            "🤖 Meta AI encountered an unexpected error.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )
