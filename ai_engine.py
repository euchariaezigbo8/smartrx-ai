import os
import requests
import streamlit as st


# ==========================================================
# SMART RX AI — META MUSE GLIMMER ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

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
            "🤖 AI explanation is currently unavailable.\n\n"
            "The Hugging Face token was not detected. "
            "Please check the HF_TOKEN secret in Streamlit."
        )

    # ======================================================
    # PREPARE AI PROMPT
    # ======================================================

    prompt = f"""
You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

You are given structured safety findings produced by
SmartRx AI's rule-based screening system.

Explain the findings clearly and simply.

IMPORTANT SAFETY RULES:

- Do not diagnose the user.
- Do not prescribe medicines.
- Do not tell the user to start or stop medication.
- Do not invent drug-herb interactions.
- Do not invent medical facts that are not present
  in the structured findings.
- Explain duplicate active ingredients clearly.
- Explain medicine-class warnings clearly.
- Explain the herbal information supplied in the findings.
- If herbal interaction information is unavailable,
  clearly state that the available database does not
  establish an interaction.
- Recommend speaking with a qualified doctor or pharmacist
  when a potential safety concern is identified.
- SmartRx AI is an educational and decision-support platform.

STRUCTURED SMART RX AI FINDINGS:

{safety_findings}

Organize the explanation using these sections:

Overall Safety Summary

Medicine Findings

Herbal Findings

Important Safety Advice

Professional Guidance

Use simple language suitable for a general Nigerian audience.
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
        # CHECK API RESPONSE
        # ==================================================

        response.raise_for_status()

        result = response.json()

        # ==================================================
        # EXTRACT AI MESSAGE
        # ==================================================

        if "choices" in result and len(result["choices"]) > 0:

            choice = result["choices"][0]

            if "message" in choice:

                content = choice["message"].get(
                    "content",
                    ""
                )

                if content:
                    return content

        return (
            "🤖 The AI service returned an unexpected response.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # TIMEOUT ERROR
    # ======================================================

    except requests.exceptions.Timeout:

        return (
            "🤖 The AI explanation service timed out.\n\n"
            "Please try the safety verification again."
        )

    # ======================================================
    # API / CONNECTION ERROR
    # ======================================================

    except requests.exceptions.RequestException as error:

        return (
            "🤖 The AI explanation service is temporarily "
            "unavailable.\n\n"
            f"Connection details: {str(error)}"
        )

    # ======================================================
    # OTHER ERROR
    # ======================================================

    except Exception as error:

        return (
            "🤖 The AI explanation service encountered "
            "an unexpected error.\n\n"
            f"Error details: {str(error)}"
        )
