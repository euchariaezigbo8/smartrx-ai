import os
import requests
import streamlit as st


# ==========================================================
# SMART RX AI — META AI ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Generates an explainable medication and herbal safety
    summary using a Meta model through Hugging Face.
    """

    # ------------------------------------------------------
    # GET HUGGING FACE TOKEN
    # ------------------------------------------------------

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
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ------------------------------------------------------
    # PREPARE FINDINGS
    # ------------------------------------------------------

    selected_medicines = safety_findings.get(
        "selected_medicines",
        []
    )

    duplicates = safety_findings.get(
        "duplicate_active_ingredients",
        []
    )

    category_warnings = safety_findings.get(
        "category_warnings",
        []
    )

    medicine_warnings = safety_findings.get(
        "medicine_warnings",
        []
    )

    selected_herbs = safety_findings.get(
        "selected_herbs",
        []
    )

    # ------------------------------------------------------
    # CREATE AI PROMPT
    # ------------------------------------------------------

    prompt = f"""
You are the AI explanation layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

Explain the structured safety findings below in clear,
simple language.

DO NOT diagnose the user.

DO NOT prescribe medicines.

DO NOT tell the user to start, stop or change medication.

DO NOT invent drug-herb interactions.

Only discuss information contained in the supplied findings.

SELECTED MEDICINES:
{selected_medicines}

DUPLICATE ACTIVE INGREDIENTS:
{duplicates}

MEDICINE CATEGORY WARNINGS:
{category_warnings}

MEDICINE WARNINGS:
{medicine_warnings}

SELECTED HERBS:
{selected_herbs}

Write the response using these sections:

Overall Safety Summary

Medicine Findings

Herbal Findings

Important Safety Advice

Professional Guidance

If information about an herb is missing, clearly say that
the SmartRx AI database does not currently contain that
information.

If no herb-drug interaction is established in the supplied
data, do not invent one.

SmartRx AI is an educational and decision-support platform
and does not replace a qualified doctor or pharmacist.
"""

    # ------------------------------------------------------
    # SEND REQUEST TO HUGGING FACE
    # ------------------------------------------------------

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

        # --------------------------------------------------
        # CHECK HTTP RESPONSE
        # --------------------------------------------------

        if response.status_code != 200:

            return (
                "🤖 The AI service could not process the "
                "request at this time.\n\n"
                f"Service response: HTTP "
                f"{response.status_code}\n\n"
                "The structured SmartRx AI safety screening "
                "has still been completed."
            )

        # --------------------------------------------------
        # READ RESPONSE
        # --------------------------------------------------

        result = response.json()

        # --------------------------------------------------
        # EXTRACT AI TEXT
        # --------------------------------------------------

        choices = result.get("choices", [])

        if choices:

            message = choices[0].get(
                "message",
                {}
            )

            content = message.get(
                "content",
                ""
            )

            if isinstance(content, str) and content.strip():

                return content.strip()

        # --------------------------------------------------
        # UNEXPECTED RESPONSE
        # --------------------------------------------------

        return (
            "🤖 The AI service returned an unexpected "
            "response.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ------------------------------------------------------
    # TIMEOUT
    # ------------------------------------------------------

    except requests.exceptions.Timeout:

        return (
            "🤖 The AI service timed out.\n\n"
            "Please try the verification again. "
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ------------------------------------------------------
    # CONNECTION ERROR
    # ------------------------------------------------------

    except requests.exceptions.RequestException:

        return (
            "🤖 SmartRx AI could not connect to the AI service.\n\n"
            "The structured safety screening has still "
            "been completed."
        )

    # ------------------------------------------------------
    # OTHER ERROR
    # ------------------------------------------------------

    except Exception as error:

        return (
            "🤖 The AI explanation service encountered "
            "an unexpected error.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )
