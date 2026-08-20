import os
import requests
import streamlit as st


# ==========================================================
# SMART RX AI — META LLAMA AI ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    # ======================================================
    # GET HUGGING FACE TOKEN
    # ======================================================

    try:
        hf_token = st.secrets["HF_TOKEN"]
    except Exception:
        hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        return (
            "🤖 The AI explanation service is not connected.\n\n"
            "Please make sure HF_TOKEN has been added to "
            "Streamlit Cloud Secrets."
        )

    # ======================================================
    # AI PROMPT
    # ======================================================

    prompt = f"""
You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

SmartRx AI has already performed structured safety screening.

Your job is to explain ONLY the information contained
in the structured findings below.

Do not invent information.

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
- Clearly explain medicine-class warnings.
- Explain the scientific names and traditional Nigerian names
  of the selected herbs.
- Explain the safety cautions stored in the SmartRx database.
- If a specific herb-drug interaction is not established by
  the supplied findings, clearly say so.
- Use simple language suitable for a general Nigerian audience.
- Recommend consultation with a qualified doctor or pharmacist
  when a safety concern is identified.

Use these sections:

### Overall Safety Summary

Briefly summarize the main findings.

### Medicine Findings

Explain the selected medicines, duplicate ingredients,
and medicine-class warnings.

### Herbal Findings

Explain the selected herbs, their scientific names,
traditional Nigerian names, and their safety cautions.

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
    # HUGGING FACE API REQUEST
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
                        "role": "system",
                        "content": (
                            "You are the safe and explainable "
                            "AI intelligence layer of SmartRx AI."
                        )
                    },
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

        if (
            "choices" in result
            and len(result["choices"]) > 0
        ):

            message = result["choices"][0].get(
                "message",
                {}
            )

            content = message.get(
                "content",
                ""
            )

            if content:
                return content.strip()

        return (
            "🤖 The AI service returned an empty response.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # HANDLE TIMEOUT
    # ======================================================

    except requests.exceptions.Timeout:

        return (
            "🤖 The AI explanation service timed out.\n\n"
            "Please try the verification again. "
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # HANDLE HTTP/API ERRORS
    # ======================================================

    except requests.exceptions.HTTPError:

        try:
            error_details = response.json()

            error_text = error_details.get(
                "error",
                "Hugging Face API request failed."
            )

        except Exception:
            error_text = (
                "Hugging Face API request failed."
            )

        return (
            "🤖 The AI explanation service could not "
            "complete the request.\n\n"
            f"API message: {error_text}\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # HANDLE CONNECTION ERRORS
    # ======================================================

    except requests.exceptions.RequestException:

        return (
            "🤖 The AI explanation service is temporarily "
            "unavailable.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # HANDLE OTHER ERRORS
    # ======================================================

    except Exception as error:

        return (
            "🤖 The AI explanation service encountered "
            "an unexpected error.\n\n"
            f"Technical message: {error}\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )
