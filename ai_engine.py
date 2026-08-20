import streamlit as st
from huggingface_hub import InferenceClient


# ==========================================================
# SMART RX AI — META LLAMA AI ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Generates an explainable safety summary for SmartRx AI
    using Meta's Llama 3.1 8B Instruct model through
    Hugging Face Inference Providers.

    The Hugging Face token is stored securely in
    Streamlit Secrets as HF_TOKEN.
    """

    # ======================================================
    # LOAD HUGGING FACE TOKEN
    # ======================================================

    try:
        hf_token = st.secrets["HF_TOKEN"]
    except Exception:
        hf_token = None

    if not hf_token:
        return (
            "🤖 The AI explanation service is not connected.\n\n"
            "Please make sure the HF_TOKEN secret has been "
            "added to Streamlit Cloud."
        )

    # ======================================================
    # AI PROMPT
    # ======================================================

    prompt = f"""
You are the AI explanation layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

SmartRx AI has already performed structured safety screening.
Your job is ONLY to explain the findings supplied below.

Do not invent information.

STRUCTURED SMART RX AI FINDINGS:

{safety_findings}

IMPORTANT SAFETY RULES:

- Do not diagnose the user.
- Do not prescribe medicines.
- Do not tell the user to start, stop, or change medication.
- Do not invent medicine-herb interactions.
- Do not invent herbal benefits or medical claims.
- Explain only information contained in the structured findings.
- Clearly identify duplicate active ingredients when present.
- Clearly explain medicine-class warnings when present.
- Explain the listed herbal scientific names and traditional names.
- Explain the safety cautions stored in the SmartRx database.
- If the database does not establish a specific herb-drug interaction,
  say that the available database does not establish one.
- Use simple language suitable for a general Nigerian audience.
- If a potential safety concern exists, recommend consultation with
  a qualified doctor or pharmacist.

Respond using these sections:

### Overall Safety Summary

Give a short summary of the main safety findings.

### Medicine Findings

Explain the selected medicines, duplicate active ingredients,
and medicine-class warnings if present.

### Herbal Findings

Explain the selected herbs, their scientific names,
traditional Nigerian names, and the safety cautions
contained in the SmartRx database.

### Important Safety Advice

Give concise safety advice based ONLY on the supplied findings.

### Professional Guidance

Explain when the user should consult a doctor or pharmacist.

Remember:

SmartRx AI is an educational and decision-support platform.
It does not replace professional medical advice.
"""

    # ======================================================
    # CONNECT TO META LLAMA THROUGH HUGGING FACE
    # ======================================================

    try:

        client = InferenceClient(
            api_key=hf_token
        )

        response = client.chat.completions.create(

            model="meta-llama/Llama-3.1-8B-Instruct",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the safe and explainable AI "
                        "intelligence layer of SmartRx AI."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=700
        )

        # ==================================================
        # EXTRACT RESPONSE
        # ==================================================

        if response and response.choices:

            content = response.choices[0].message.content

            if content:

                return content.strip()

        return (
            "🤖 The AI model returned an empty response.\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )

    # ======================================================
    # HANDLE AUTHENTICATION ERRORS
    # ======================================================

    except Exception as error:

        error_message = str(error)

        # Do not expose the Hugging Face token
        if hf_token in error_message:
            error_message = error_message.replace(
                hf_token,
                "[HIDDEN]"
            )

        return (
            "🤖 The AI explanation service could not "
            "complete the request.\n\n"
            f"Technical information: {error_message}\n\n"
            "The structured SmartRx AI safety screening "
            "has still been completed."
        )
