import os
import json
import requests


# ==========================================================
# SMART RX AI — META AI EXPLANATION ENGINE
# ==========================================================

def generate_ai_explanation(safety_findings):

    """
    Generates an explainable medication and herbal safety
    summary using the configured Meta/Groq AI model.

    The AI receives structured findings from app.py and
    explains them without inventing medical relationships.
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

    selected_medicines = safety_findings.get(
        "selected_medicines",
        []
    )

    duplicate_active_ingredients = safety_findings.get(
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

    herb_drug_interactions = safety_findings.get(
        "herb_drug_interactions",
        []
    )

    # IMPORTANT:
    # This is the new structured finding that handles
    # relationships such as:
    #
    # Artemisia annua
    # Artemisinin
    #        ↓
    # Artemether
    #
    # It is NOT treated as a duplicate ingredient.

    compound_relationships = safety_findings.get(
        "compound_overlaps",
        []
    )

    selected_herbs = safety_findings.get(
        "selected_herbs",
        []
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

        "compound_relationships":
            compound_relationships,

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

You MUST distinguish clearly between:

1. Duplicate active ingredients
2. Medicine-class warnings
3. Stored herb-drug interaction findings
4. Active compound / drug-derivative relationships
5. Stored medicine safety information
6. Herbal active compounds
7. General herbal safety cautions

CRITICAL RULE:

A compound relationship is NOT automatically a drug interaction.

For example:

Artemisia annua contains artemisinin.

Artemether is an artemisinin derivative used in
artemisinin-based antimalarial medicines.

Therefore, a finding involving:

Artemisinin ↔ Artemether

must NOT be described as:

- a duplicate active ingredient
- the same ingredient
- proof of a harmful interaction
- proof that the herb and medicine are unsafe together

Instead describe it as a:

"potential active compound / drug-derivative relationship"

and explain that professional review is appropriate before
combining an Artemisia preparation with an artemisinin-based
antimalarial medicine.

Do not invent interactions, ingredients, scientific names,
risk levels, evidence or medical claims that are not present
in the supplied structured findings.

Use ONLY the supplied structured findings.

If no stored herb-drug interaction is present but a compound
relationship is present, DO NOT say that no herb-related
finding exists.

Instead clearly distinguish:

"Stored herb-drug interaction findings: none identified."

from:

"Potential active compound / drug-derivative relationships:
identified."

Do not convert one category into another.

Organise your response using these sections:

### Overall Safety Summary

Give a concise summary of the major findings.

Mention whether the screening identified:

- duplicate active ingredients
- medicine-class warnings
- stored herb-drug interaction findings
- active compound / drug-derivative relationships

Do not exaggerate the significance of any finding.

### Medicine Findings

Explain:

- duplicate active ingredients
- medicines involved
- active ingredients
- medicine-class warnings
- medicine-specific safety information

For NSAIDs specifically, identify the actual medicines
detected and their active ingredients.

### Herbal Findings

For each selected herb explain:

- herb name
- scientific name
- major active compounds
- traditional Nigerian names
- safety caution

### Herb–Drug Interaction Findings

Only discuss findings contained in the
"herb_drug_interactions" data.

For each detected interaction explain:

- herb
- affected orthodox medicines
- drug class
- major active compounds
- risk level
- evidence note

Do not describe an interaction as proven if the supplied
evidence only describes it as potential or cautionary.

If this list is empty, say that no stored herb-drug interaction
flag was identified.

### Active Compound / Drug-Derivative Relationships

Discuss only the relationships contained in
"compound_relationships".

For each relationship explain:

- herb
- medicine
- herb-associated compound
- medicine-associated ingredient or derivative
- why the relationship is pharmacologically relevant
- that the relationship does NOT by itself prove a harmful
  interaction

For Artemisia annua and artemisinin-based medicines, make
the distinction between artemisinin and artemether clear.

Do not call artemisinin and artemether the same active
ingredient.

### Important Safety Advice

Provide practical educational safety guidance based ONLY
on the supplied findings.

State that herbal products should not automatically be
assumed to be safe simply because they are natural.

State that a compound relationship does not by itself prove
that a combination is unsafe.

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

IMPORTANT:

Do not reinterpret the structured findings.

Do not create an interaction that is not present.

Do not turn an active compound / drug-derivative relationship
into a duplicate ingredient warning.

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
                "model":
                    model_name,

                "messages": [
                    {
                        "role":
                            "system",

                        "content":
                            system_prompt
                    },

                    {
                        "role":
                            "user",

                        "content":
                            user_prompt
                    }
                ],

                "temperature":
                    0.2,

                "max_tokens":
                    1800
            },

            timeout=60
        )


        response.raise_for_status()

        result = response.json()


        # ==================================================
        # EXTRACT AI RESPONSE
        # ==================================================

        return (
            result[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )


    except Exception:

        return build_structured_fallback(
            safety_findings
        )


# ==========================================================
# STRUCTURED FALLBACK
# ==========================================================

def build_structured_fallback(safety_findings):

    """
    Creates a structured explanation when the external
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

    compound_relationships = safety_findings.get(
        "compound_overlaps",
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
            "The screening identified medicine-class "
            "warnings that should be reviewed carefully."
        )


    if interactions:

        summary_parts.append(
            "Stored potential herb-drug interaction findings "
            "were identified for some selected herbs and medicines."
        )


    if compound_relationships:

        summary_parts.append(
            "The screening also identified potential active "
            "compound or drug-derivative relationships. "
            "These relationships do not by themselves prove "
            "that a combination is unsafe."
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


    # ------------------------------------------------------
    # DUPLICATES
    # ------------------------------------------------------

    if duplicates:

        output.append(
            "\n\n**Duplicate Active Ingredients:**"
        )


        for item in duplicates:

            output.append(
                f"\n- {item['ingredient']}: "
                f"{', '.join(item['medicines'])}"
            )


    # ------------------------------------------------------
    # CLASS WARNINGS
    # ------------------------------------------------------

    if category_warnings:

        output.append(
            "\n\n**Medicine-Class Warnings:**"
        )


        for warning in category_warnings:

            output.append(
                f"\n- {warning}"
            )


    # ------------------------------------------------------
    # MEDICINE-SPECIFIC WARNINGS
    # ------------------------------------------------------

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
    # STORED HERB–DRUG INTERACTIONS
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
            "\nNo stored herb-drug interaction flag "
            "was identified for the selected combination."
        )


    # ======================================================
    # ACTIVE COMPOUND / DRUG-DERIVATIVE RELATIONSHIPS
    # ======================================================

    output.append(
        "\n### Active Compound / Drug-Derivative Relationships"
    )


    if compound_relationships:

        for item in compound_relationships:

            herb_name = item.get(
                "herb",
                "Unknown herb"
            )

            medicine_name = item.get(
                "medicine",
                "Unknown medicine"
            )

            compound = item.get(
                "compound",
                "Unknown compound"
            )

            medicine_ingredient = item.get(
                "medicine_ingredient",
                item.get(
                    "drug_ingredient",
                    "Not specified"
                )
            )


            output.append(
                f"\n- **{herb_name} + {medicine_name}**"
            )


            output.append(
                f"\n  - Herb-associated compound: "
                f"{compound}"
            )


            output.append(
                f"\n  - Medicine-associated ingredient: "
                f"{medicine_ingredient}"
            )


            # Special explanation for Artemisia relationships

            if (
                str(compound).lower()
                == "artemisinin"
                and
                "artemether"
                in str(
                    medicine_ingredient
                ).lower()
            ):

                output.append(
                    "\n  - Relationship: Artemisinin is "
                    "associated with Artemisia annua, while "
                    "artemether is an artemisinin derivative "
                    "used in artemisinin-based antimalarial "
                    "medicines."
                )


                output.append(
                    "\n  - Important distinction: "
                    "Artemisinin and artemether are not the "
                    "same active ingredient. This finding does "
                    "not represent duplicate ingredients."
                )


            else:

                output.append(
                    "\n  - Interpretation: This is a "
                    "pharmacologically relevant compound "
                    "relationship identified by the SmartRx "
                    "screening rules."
                )


            output.append(
                "\n  - Safety interpretation: "
                "A compound relationship alone does not prove "
                "that the combination is harmful or unsafe. "
                "Professional review is recommended before "
                "combining medicinal herbal preparations with "
                "prescription medicines."
            )


    else:

        output.append(
            "\nNo active compound or drug-derivative "
            "relationship was identified."
        )


    # ======================================================
    # IMPORTANT SAFETY ADVICE
    # ======================================================

    output.append(
        """
### Important Safety Advice

Review duplicate active ingredients, medicine-class
warnings, stored herb-drug interaction findings and
potential active compound relationships carefully.

Herbal products should not automatically be assumed
to be safe simply because they are natural.

A pharmacological compound relationship does not by
itself prove that a combination is unsafe.

Where SmartRx AI identifies a potential interaction or
compound relationship, discuss the relevant medicines
and herbs with a qualified healthcare professional.
"""
    )


    # ======================================================
    # PROFESSIONAL GUIDANCE
    # ======================================================

    output.append(
        """
### Professional Guidance

SmartRx AI provides educational and decision-support
information.

It does not diagnose medical conditions or replace a
qualified doctor or pharmacist.

Consult a qualified healthcare professional for
personalised medical advice before starting, stopping
or combining medicines or herbal products.
"""
    )


    return "\n".join(output)
