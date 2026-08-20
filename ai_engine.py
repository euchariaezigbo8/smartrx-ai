import streamlit as st                                                  
import pandas as pd                                                     
from ai_engine import generate_ai_explanation                           

# ==========================================================

# SMART RX AI — META MUSE GLIMMER ENGINE

# ==========================================================
def generate_ai_explanation(safety_findings):
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

prompt = f"""
```

You are the AI intelligence layer of SmartRx AI,
a Nigerian medication and herbal safety intelligence platform.

You are given structured findings from the SmartRx AI safety engine.

Explain ONLY the information contained in those findings.

Do not diagnose the user.
Do not prescribe medicines.
Do not recommend starting, stopping, or changing medication.
Do not invent drug-herb interactions.
Do not claim an interaction exists unless it appears in the findings.
Clearly identify uncertainty or missing information.
Use simple language suitable for a general Nigerian audience.
Recommend consultation with a qualified doctor or pharmacist
when a safety concern is identified.

STRUCTURED FINDINGS:

{safety_findings}

Use these sections:

### Overall Safety Summary

### Medicine Findings

### Herbal Findings

### Important Safety Advice

### Professional Guidance

SmartRx AI is an educational and decision-support platform.
It does not replace professional medical advice.
"""

```
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

except requests.exceptions.Timeout:
    return (
        "🤖 The AI explanation service timed out.\n\n"
        "Please try the safety verification again. "
        "The structured SmartRx AI safety screening "
        "remains available."
    )

except requests.exceptions.RequestException:
    return (
        "🤖 The AI explanation service is temporarily "
        "unavailable.\n\n"
        "The structured SmartRx AI safety screening "
        "remains available."
    )

except Exception:
    return (
        "🤖 The AI explanation service encountered an "
        "unexpected error.\n\n"
        "The structured SmartRx AI safety screening "
        "remains available."
    )
