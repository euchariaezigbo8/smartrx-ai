import os
import json
import requests


# ==========================================================
# SMART RX AI — META AI EXPLANATION ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Generates an explainable medication and herbal safety
    summary using the configured Meta AI model.

    The AI receives structured findings from app.py and
    explains them in user-friendly language.
    """

    # ======================================================
    # LOAD API CONFIGURATION
    # ======================================================

    api_key = os.getenv("META_AI_API_KEY")

    model_name = os.getenv(
        "META_AI_MODEL",
        "meta-llama/llama-3.1-8b-instruct"
    )


    # ======================================================
    # FALLBACK IF API KEY IS NOT AVAILABLE
    # ======================================================

    if not api_key:

        return build_structured_fallback(
            safety_findings
        )


    # ======================================================
    # EXTRACT STRUCTURED FINDINGS
    # ======================================================

    selected_medicines = (
        safety_findings.get(
            "selected_medicines",
            []
        )
    )

    duplicate_active_ingredients = (
        safety_findings.get(
            "duplicate_active_ingredients",
            []
        )
    )

    category_warnings = (
        safety_findings.get(
            "category_warnings",
            []
        )
    )

    medicine_warnings = (
        safety_findings.get(
            "medicine_warnings",
            []
        )
    )

    herb_drug_interactions = (
        safety_findings.get(
            "herb_drug_interactions",
            []
        )
    )

    selected_herbs = (
        safety_findings.get(
            "selected_herbs",
            []
        )
    )


    # ======================================================
    # PREPARE STRUCTURED DATA FOR AI
    # ======================================================

    structured_data = {

        "selected_medicines":
            selected_medicines,

        "duplicate_active_ingredients":
            duplicate_active_ingredients,

        "medicine_class_warnings":
            category_warnings,

        "medicine_warnings":
            medicine_warnings,

        "herb_drug_interactions":
            herb_drug_interactions,

        "selected_herbs":
            selected_herbs
    }


    # ======================================================
    # AI SYSTEM INSTRUCTIONS
    # ======================================================

    system_prompt = """
You are SmartRx AI, an explainable medication and herbal
safety intelligence assistant.

Your role is to explain structured safety-screening findings
in clear, cautious and understandable language.

You MUST NOT diagnose diseases.

You MUST NOT prescribe medicines.

You MUST NOT tell a user to start, stop or change a medicine.

You MUST distinguish between:
- detected duplicate active ingredients
- medicine-class warnings
- potential herb-drug interactions
- stored medicine safety information
- herbal active compounds
- general safety cautions

Do not invent interactions, ingredients, scientific names,
risk levels or evidence that are not present in the supplied
structured findings.

Use only the information provided.

Organise your response using these sections:

### Overall Safety Summary

Give a concise summary of the major findings.

### Medicine Findings

Explain:
- duplicate active ingredients
- medicines involved
- active ingredients
- medicine-class warnings
- medicine-specific safety information

For NSAIDs specifically, identify the actual medicines detected
and their active ingredients.

### Herbal Findings

For each selected herb explain:
- herb name
- scientific name
- major active compounds
- traditional Nigerian names
- safety caution

### Herb–Drug Interaction Findings

For each detected interaction explain:
- herb
- affected orthodox medicines
- drug class
- major active compounds
- risk level
- evidence note

Do not describe an interaction as proven if the supplied
evidence only describes it as a potential or cautionary risk.

### Important Safety Advice

Provide practical educational safety guidance based ONLY
on the supplied findings.

### Professional Guidance

Remind the user to consult a qualified doctor or pharmacist
for personalised medical advice.

Keep the tone professional, clear and appropriate for a
healthcare technology demonstration.
"""


    # ======================================================
    # USER PROMPT
    # ======================================================

    user_prompt = f"""
Analyse the following SmartRx AI structured screening results.

Return a clear, explainable safety report using the sections
specified in your instructions.

STRUCTURED SCREENING RESULTS:

{json.dumps(
    structured_data,
    indent=2,
    default=str
)}
"""


    # ======================================================
    # API REQUEST
    # ======================================================

    try:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization":
                    f"Bearer {api_key}",

                "Content-Type":
                    "application/json"
            },

            json={
                "model": model_name,

                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],

                "temperature": 0.2,

                "max_tokens": 1500
            },

            timeout=60
        )


        response.raise_for_status()


        result = response.json()


        # ==================================================
        # EXTRACT AI RESPONSE
        # ==================================================

        return (
            result["choices"][0]["message"]["content"]
        )


    except Exception as error:

        return build_structured_fallback(
            safety_findings
        )


# ==========================================================
# STRUCTURED FALLBACK
# ==========================================================

def build_structured_fallback(safety_findings):

    """
    Creates a useful structured explanation when the external
    AI service is unavailable.
    """

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

    interactions = safety_findings.get(
        "herb_drug_interactions",
        []
    )

    herbs = safety_findings.get(
        "selected_herbs",
        []
    )


    # ======================================================
    # OVERALL SUMMARY
    # ======================================================

    summary_parts = []


    if duplicates:

        summary_parts.append(
            "The screening identified duplicate active "
            "ingredients among some of the selected medicines."
        )


    if category_warnings:

        summary_parts.append(
            "The screening also identified medicine-class "
            "warnings that should be reviewed carefully."
        )


    if interactions:

        summary_parts.append(
            "Potential herb–drug interaction flags were "
            "identified for some selected herbs and medicines."
        )


    if not summary_parts:

        summary_parts.append(
            "No major issue was identified by the current "
            "structured screening rules."
        )


    output = []


    output.append(
        "### Overall Safety Summary\n\n"
        + " ".join(summary_parts)
    )


    # ======================================================
    # MEDICINE FINDINGS
    # ======================================================

    output.append(
        "\n### Medicine Findings"
    )


    if selected_medicines:

        output.append(
            "\nSelected medicines: "
            + ", ".join(selected_medicines)
            + "."
        )


    if duplicates:

        output.append(
            "\n\n**Duplicate Active Ingredients:**"
        )


        for item in duplicates:

            output.append(
                f"\n- {item['ingredient']}: "
                f"{', '.join(item['medicines'])}"
            )


    if category_warnings:

        output.append(
            "\n\n**Medicine-Class Warnings:**"
        )


        for warning in category_warnings:

            output.append(
                f"\n- {warning}"
            )


    if medicine_warnings:

        output.append(
            "\n\n**Medicine-Specific Safety Information:**"
        )


        for item in medicine_warnings:

            output.append(
                f"\n- **{item['medicine']}** — "
                f"Active ingredient: {item['ingredient']}; "
                f"Class: {item['category']}; "
                f"{item['warning']}"
            )


    # ======================================================
    # HERBAL FINDINGS
    # ======================================================

    output.append(
        "\n### Herbal Findings"
    )


    if herbs:

        for herb in herbs:

            output.append(
                f"\n- **{herb['herb']}** "
                f"(*{herb['scientific_name']}*)"
            )

            output.append(
                f"\n  - Traditional Names: "
                f"{herb['traditional_names']}"
            )

            output.append(
                f"\n  - Major Active Compounds: "
                f"{herb['active_compounds']}"
            )

            output.append(
                f"\n  - Safety Caution: "
                f"{herb['safety_caution']}"
            )

    else:

        output.append(
            "\nNo herbs were selected."
        )


    # ======================================================
    # HERB–DRUG INTERACTIONS
    # ======================================================

    output.append(
        "\n### Herb–Drug Interaction Findings"
    )


    if interactions:

        for item in interactions:

            output.append(
                f"\n- **{item['herb']} + "
                f"{item['drug_class']} medicines**"
            )

            output.append(
                f"\n  - Orthodox Medicines: "
                f"{', '.join(item['medicines'])}"
            )

            output.append(
                f"\n  - Major Active Compounds: "
                f"{item['active_compounds']}"
            )

            output.append(
                f"\n  - Risk Level: "
                f"{item['risk']}"
            )

            output.append(
                f"\n  - Evidence Note: "
                f"{item['evidence']}"
            )

    else:

        output.append(
            "\nNo stored herb–drug interaction flag "
            "was identified for the selected combination."
        )


    # ======================================================
    # IMPORTANT SAFETY ADVICE
    # ======================================================

    output.append(
        """
### Important Safety Advice

Review duplicate active ingredients and medicine-class
warnings carefully. Herbal products should not automatically
be assumed to be safe simply because they are natural.

Where a potential herb–drug interaction has been flagged,
the relevant medicines and herbs should be discussed with
a qualified healthcare professional.
"""
    )


    # ======================================================
    # PROFESSIONAL GUIDANCE
    # ======================================================

    output.append(
        """
### Professional Guidance

SmartRx AI provides educational and decision-support
information. Consult a qualified doctor or pharmacist
for personalised medical advice before making medication
decisions.
"""
    )


    return "\n".join(output)
