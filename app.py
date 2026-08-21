import streamlit as st
import pandas as pd
from ai_engine import generate_ai_explanation


# ==========================================================
# SMART RX AI — PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="SmartRx AI",
    page_icon="💊",
    layout="wide"
)


# ==========================================================
# LOAD HERBAL MEDICINE DATABASE
# ==========================================================

try:
    herbs_df = pd.read_csv("herbs.csv")
except FileNotFoundError:
    st.error(
        "herbs.csv not found. Please make sure it is "
        "in the same repository folder as app.py."
    )
    st.stop()


required_herb_columns = [
    "Herb",
    "Scientific",
    "Yoruba",
    "Hausa",
    "Igbo",
    "Category",
    "Active_Compounds",
    "Interaction_Class",
    "Safety_Caution"
]

missing_herb_columns = [
    column
    for column in required_herb_columns
    if column not in herbs_df.columns
]

if missing_herb_columns:
    st.error(
        "The following columns are missing from herbs.csv: "
        + ", ".join(missing_herb_columns)
    )
    st.stop()


herb_list = sorted(
    herbs_df["Herb"]
    .dropna()
    .unique()
    .tolist()
)


# ==========================================================
# LOAD MEDICATION DATABASE
# ==========================================================

try:
    medicines_df = pd.read_csv("medicines.csv")
except FileNotFoundError:
    st.error(
        "medicines.csv not found. Please make sure it is "
        "in the same repository folder as app.py."
    )
    st.stop()


# ==========================================================
# LOAD HERB–DRUG INTERACTION DATABASE
# ==========================================================

try:
    interactions_df = pd.read_csv("interactions.csv")
except FileNotFoundError:
    st.error(
        "interactions.csv not found. Please add it to the project folder."
    )
    st.stop()


required_medicine_columns = [
    "Medicine",
    "Ingredient",
    "Category",
    "Warning"
]

missing_medicine_columns = [
    column
    for column in required_medicine_columns
    if column not in medicines_df.columns
]

if missing_medicine_columns:
    st.error(
        "The following columns are missing from medicines.csv: "
        + ", ".join(missing_medicine_columns)
    )
    st.stop()

medicine_list = sorted(
    medicines_df["Medicine"]
    .dropna()
    .unique()
    .tolist()
)


# ==========================================================
# SMART RX AI — CUSTOM STYLING
# ==========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #FAFBFC;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        background: linear-gradient(
            135deg,
            #4338CA,
            #6366F1
        );

        color: white;
        padding: 35px;
        border-radius: 20px;
        border-left: 10px solid #F9CC48;
        margin-bottom: 25px;

        box-shadow:
            0 8px 32px rgba(31, 38, 135, 0.20);
    }

    .hero h1,
    .hero h3,
    .hero p {
        color: white !important;
    }


    /* ======================================================
       GENERAL CARDS
       ====================================================== */

    .card {
        background: #FFFFFF;
        border: 1px solid rgba(20,70,124,0.10);

        box-shadow:
            0 12px 35px rgba(0,0,0,0.08);

        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
    }


    /* ======================================================
       SECTION BOX
       ====================================================== */

    .section {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 20px;

        border: 1px solid rgba(20,70,124,0.10);

        box-shadow:
            0 8px 25px rgba(0,0,0,0.06);

        margin-bottom: 20px;
    }


    /* ======================================================
       SAFETY BOXES
       ====================================================== */

    .safe {
        background-color: #D1FAE5;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #16A34A;
        margin-bottom: 15px;
    }

    .warning {
        background-color: #FEF3C7;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #F59E0B;
        margin-bottom: 15px;
    }

    .danger {
        background-color: #FEE2E2;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #DC2626;
        margin-bottom: 15px;
    }


    /* ======================================================
       AI RESULT BOX
       ====================================================== */

    .ai-box {
        background: #EEF2FF;
        padding: 25px;
        border-radius: 18px;
        border-left: 8px solid #4338CA;

        margin-top: 20px;
        margin-bottom: 20px;

        box-shadow:
            0 8px 25px rgba(67,56,202,0.10);
    }


    /* ======================================================
       SAFETY VERIFICATION BUTTON
       ====================================================== */

    div.stButton > button {
        width: 100%;

        background: linear-gradient(
            135deg,
            #4338CA,
            #6366F1
        );

        color: white;

        font-size: 20px;
        font-weight: 800;

        padding: 18px 25px;

        border: none;
        border-radius: 14px;

        box-shadow:
            0 8px 20px rgba(67,56,202,0.25);

        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 25px rgba(67,56,202,0.35);
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #111111;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        padding: 25px;

        color: #555555;

        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

st.sidebar.title("💊 SmartRx AI")

st.sidebar.caption(
    "AI-Powered Medication & Herbal Safety Intelligence"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "ℹ️ About",
        "📘 How To Use",
        "🔍 AI Safety Checker"
    ]
)


# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown(
        """
        <div class="hero">

        <h1>💊 SmartRx AI</h1>

        <h3>
        AI-Powered Medication & Herbal Safety Intelligence
        </h3>

        <p>
        SmartRx AI is an intelligent medication-safety platform
        designed to help users understand potential risks involving
        orthodox medicines, traditional African medicinal herbs,
        duplicate active ingredients and medication combinations.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="card">

            <h3>💊 Medication Intelligence</h3>

            <p>
            Analyse multiple medicines and identify duplicate
            active ingredients and potential medication conflicts.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="card">

            <h3>🌿 Herbal Intelligence</h3>

            <p>
            Cross-reference Nigerian traditional medicinal herbs
            with pharmaceutical medicines using a structured
            ethnobotanical safety knowledge base.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="card">

            <h3>🤖 Meta AI Intelligence</h3>

            <p>
            Use Meta AI intelligence to generate explainable
            safety summaries from structured medication and
            herbal screening results.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        """
        <div class="section">

        <h2 style="color:#4338CA;">
        Why SmartRx AI?
        </h2>

        <p>
        Many medicines can contain similar active ingredients,
        while traditional herbal preparations may also contain
        biologically active compounds.
        </p>

        <p>
        SmartRx AI combines structured medication information,
        ethnobotanical knowledge and artificial intelligence to
        provide clearer safety information for users.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# ABOUT PAGE
# ==========================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About SmartRx AI")

    st.markdown(
        """
        <div class="section">

        <h2 style="color:#4338CA;">
        The Innovation
        </h2>

        <p>
        <strong>SmartRx AI</strong> is an AI-powered medication
        and herbal safety intelligence platform developed by
        <strong>Chizix Orbit Digital Innovations Ltd.</strong>
        </p>

        <p>
        The platform is designed to bridge pharmaceutical
        medication information with Traditional African Medicine
        by combining structured safety knowledge with artificial
        intelligence.
        </p>

        <p>
        SmartRx AI uses <strong>Meta AI models</strong> as an
        AI intelligence and explanation layer, helping transform
        structured safety findings into understandable information
        for users.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="section">

        <h3 style="color:#4338CA;">
        Core Capabilities
        </h3>

        <p>💊 Orthodox medicine intelligence</p>
        <p>🌿 Nigerian herbal medicine intelligence</p>
        <p>🔬 Active ingredient analysis</p>
        <p>⚠️ Medication duplication screening</p>
        <p>🌿 Herb–drug safety information</p>
        <p>🤖 Meta AI-powered explanations</p>
        <p>🇳🇬 Nigerian-focused health innovation</p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.info(
        "SmartRx AI is an educational and decision-support "
        "platform. It does not replace a qualified doctor, "
        "pharmacist or other healthcare professional."
    )


# ==========================================================
# HOW TO USE PAGE
# ==========================================================

elif page == "📘 How To Use":

    st.title("📘 How To Use SmartRx AI")


    steps = [
        (
            "Step 1 — Select Your Medicines",
            "Go to AI Safety Checker and select the orthodox "
            "medicines you want to screen."
        ),
        (
            "Step 2 — Select Your Herbs",
            "Select up to four Nigerian or Traditional African "
            "medicinal herbs from the herb selector."
        ),
        (
            "Step 3 — Run Safety Screening",
            "Click the prominent AI Safety Verification button "
            "to analyse the selected medicines and herbs."
        ),
        (
            "Step 4 — Review Structured Findings",
            "SmartRx AI checks for duplicate active ingredients, "
            "medicine-class conflicts and stored safety warnings."
        ),
        (
            "Step 5 — Read the AI Explanation",
            "The Meta AI layer explains the structured findings "
            "in clearer, user-friendly language."
        ),
        (
            "Step 6 — Seek Professional Advice",
            "Use the results as educational safety information "
            "and consult a qualified healthcare professional "
            "before making medication decisions."
        )
    ]


    for title, description in steps:

        st.markdown(
            f"""
            <div class="section">

            <h3 style="color:#4338CA;">
            {title}
            </h3>

            <p>
            {description}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================================
# AI SAFETY CHECKER
# ==========================================================

elif page == "🔍 AI Safety Checker":

    st.title("🔍 AI Safety Checker")

    # ======================================================
    # INTRODUCTION
    # ======================================================

    st.markdown(
        """
        <div class="section">

        <h3 style="color:#4338CA;">
        Medication & Herbal Safety Verification
        </h3>

        <p>
        Select the medicines and Nigerian or Traditional African
        medicinal herbs you want SmartRx AI to analyse.
        The system screens the selected medicines and herbs for
        duplicate active ingredients, medicine-class conflicts,
        potential herb–drug interactions, stored safety warnings
        and major herbal active compounds.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================================
    # 1. SELECT MEDICINES
    # ======================================================

    st.subheader("💊 1. Select Your Medicines")

    st.write(
        "Select up to five orthodox medicines for safety screening."
    )

    selected_medicines = st.multiselect(
        "Choose medicines",
        medicine_list,
        max_selections=5,
        placeholder="Search and select up to five medicines..."
    )


        # ======================================================
    # 2. SELECT HERBS
    # ======================================================

    st.subheader(
        "🌿 2. Select Nigerian / Traditional African Herbs"
    )

    st.write(
        "Select up to four Nigerian or Traditional African "
        "medicinal herbs for safety screening."
    )

    herb_slots = []

    for i in range(4):

        herb = st.selectbox(
            f"Herb {i + 1}",
            [""] + herb_list,
            key=f"herb_slot_{i}"
        )

        if herb:
            herb_slots.append(herb)

    # Remove duplicate herb selections
    selected_herbs = list(dict.fromkeys(herb_slots))


    # ======================================================
    # RUN SAFETY SCREENING
    # ======================================================

    if st.button(
        "🤖 RUN AI SAFETY VERIFICATION",
        use_container_width=True
    ):

        if not selected_medicines:

            st.warning(
                "Please select at least one medicine."
            )

        else:

            # ==================================================
            # SELECTED MEDICINES
            # ==================================================

            chosen = medicines_df[
                medicines_df["Medicine"].isin(
                    selected_medicines
                )
            ].copy()

            st.subheader(
                "📋 Selected Medicines & Safety Screening Results"
            )

            medicine_table = chosen[
                [
                    "Medicine",
                    "Ingredient",
                    "Category",
                    "Warning"
                ]
            ].copy()

            medicine_table.columns = [
                "Medicine",
                "Active Ingredient",
                "Drug Class",
                "Safety Warning"
            ]

            st.dataframe(
                medicine_table,
                use_container_width=True,
                hide_index=True
            )


            # ==================================================
            # SELECTED HERBS
            # ==================================================

            selected_herb_data = herbs_df[
                herbs_df["Herb"].isin(
                    selected_herbs
                )
            ].copy()

            if not selected_herb_data.empty:

                st.subheader(
                    "🌿 Selected Herbs & Herbal Safety Summary"
                )

                herb_table = selected_herb_data[
                    [
                        "Herb",
                        "Scientific",
                        "Yoruba",
                        "Hausa",
                        "Igbo",
                        "Active_Compounds",
                        "Safety_Caution"
                    ]
                ].copy()

                herb_table["Traditional Names"] = (
                    "Yoruba: "
                    + herb_table["Yoruba"].fillna("Not available")
                    + " • Hausa: "
                    + herb_table["Hausa"].fillna("Not available")
                    + " • Igbo: "
                    + herb_table["Igbo"].fillna("Not available")
                )

                herb_table = herb_table[
                    [
                        "Herb",
                        "Scientific",
                        "Traditional Names",
                        "Active_Compounds",
                        "Safety_Caution"
                    ]
                ]

                herb_table.columns = [
                    "Herb",
                    "Scientific Name",
                    "Traditional Names",
                    "Major Active Compounds",
                    "Safety Caution"
                ]
                st.dataframe(
                    herb_table,
                    use_container_width=True,
                    hide_index=True
                )

            # ==================================================
            # AI CLINICAL SAFETY ANALYSIS
            # ==================================================

            st.subheader("🧠 AI Clinical Safety Analysis")

            # Paste the 🔴 🟠 🟡 🟣 analysis code immediately below this

            # ==================================================
            # DUPLICATE ACTIVE INGREDIENT ANALYSIS
            # ==================================================

            ingredient_count = {}

            for ingredient in chosen["Ingredient"].dropna():

                ingredients = [
                    item.strip()
                    for item in str(ingredient).split("+")
                    if item.strip()
                ]

                for item in ingredients:

                    ingredient_count[item] = (
                        ingredient_count.get(item, 0) + 1
                    )

            duplicates = [
                ingredient
                for ingredient, count
                in ingredient_count.items()
                if count > 1
            ]

            duplicate_details = []

            for ingredient in duplicates:

                medicines_with_ingredient = []

                for _, medicine_row in chosen.iterrows():

                    medicine_ingredients = [
                        item.strip()
                        for item in str(
                            medicine_row["Ingredient"]
                        ).split("+")
                        if item.strip()
                    ]

                    if ingredient in medicine_ingredients:

                        medicines_with_ingredient.append(
                            medicine_row["Medicine"]
                        )

                duplicate_details.append(
                    {
                        "ingredient": ingredient,
                        "medicines": medicines_with_ingredient
                    }
                )


            # ==================================================
            # DUPLICATE INGREDIENT DISPLAY
            # ==================================================

            if duplicates:

                st.markdown(
                    """
                    <div class="danger">

                    <h3>
                    🚨 Duplicate Active Ingredient Detected
                    </h3>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                for duplicate_detail in duplicate_details:

                    st.write(
                        f"**Duplicate Active Ingredient: {duplicate_detail['ingredient']}**"
                    )

                    st.write(
                        "Found in: "
                        + ", ".join(
                            duplicate_detail["medicines"]
                        )
                    )
            # ==================================================
            # CATEGORY ANALYSIS
            # ==================================================

            categories = (
                chosen["Category"]
                .dropna()
                .astype(str)
                .str.strip()
                .str.upper()
                .tolist()
            )


            category_warnings = []


            # ==================================================
            # NSAID DETECTION
            # ==================================================

            nsaid_medicines = chosen[
                chosen["Category"]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq("NSAID")
            ].copy()


            if len(nsaid_medicines) > 1:

                nsaid_names = nsaid_medicines[
                    "Medicine"
                ].tolist()


                category_warnings.append(
                    "Multiple NSAID medicines were selected. "
                    "Combining NSAIDs may increase the risk "
                    "of stomach irritation and bleeding."
                )


            # ==================================================
            # MEDICINE WARNINGS
            # ==================================================

            medicine_warnings = []

            for _, row in chosen.iterrows():

                warning = row["Warning"]

                if pd.isna(warning):

                    warning = "No specific warning available."

                medicine_warnings.append(
                    {
                        "medicine": row["Medicine"],
                        "ingredient": row["Ingredient"],
                        "category": row["Category"],
                        "warning": warning
                    }
                )


            # ==================================================
            # DISPLAY CATEGORY WARNINGS
            # ==================================================

            if category_warnings:

                st.markdown(
                    """
                    <div class="warning">

                    <h3>
                    ⚠️ Medicine Combination Warning
                    </h3>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                for warning in category_warnings:

                    st.write(warning)


                if len(nsaid_medicines) > 1:

                    st.markdown(
                        """
                        <div class="section">

                        <h4 style="color:#DC2626;">
                        💊 NSAID Medicines Detected
                        </h4>

                        """,
                        unsafe_allow_html=True
                    )


                    for _, row in nsaid_medicines.iterrows():

                        st.markdown(
                            f"""
                            <p>
                            <strong>Medicine:</strong>
                            {row["Medicine"]}
                            <br>

                            <strong>Active Ingredient:</strong>
                            {row["Ingredient"]}
                            <br>

                            <strong>Drug Class:</strong>
                            {row["Category"]}
                            </p>
                            """,
                            unsafe_allow_html=True
                        )


                    st.markdown(
                        """
                        <p>
                        <strong>Safety Note:</strong>
                        Multiple NSAID medicines were selected.
                        Combining NSAIDs may increase the risk
                        of stomach irritation and bleeding.
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

           
            # ==================================================
            # HERBAL SAFETY INFORMATION
            # ==================================================

            herbal_findings = []


            for _, herb_row in selected_herb_data.iterrows():

                scientific = herb_row["Scientific"]

                active_compounds = herb_row["Active_Compounds"]

                yoruba = herb_row["Yoruba"]

                hausa = herb_row["Hausa"]

                igbo = herb_row["Igbo"]

                safety_caution = herb_row["Safety_Caution"]


                if pd.isna(scientific) or not str(scientific).strip():
                    scientific = "Not available"

                if (
                    pd.isna(active_compounds)
                    or not str(active_compounds).strip()
                ):
                    active_compounds = "Not available"

                if pd.isna(yoruba) or not str(yoruba).strip():
                    yoruba = "Not available"

                if pd.isna(hausa) or not str(hausa).strip():
                    hausa = "Not available"

                if pd.isna(igbo) or not str(igbo).strip():
                    igbo = "Not available"

                if (
                    pd.isna(safety_caution)
                    or not str(safety_caution).strip()
                ):
                    safety_caution = (
                        "No safety caution available."
                    )


                traditional_names = (
                    f"Yoruba: {yoruba} • "
                    f"Hausa: {hausa} • "
                    f"Igbo: {igbo}"
                )


                herbal_findings.append(
                    {
                        "herb": herb_row["Herb"],
                        "scientific_name": scientific,
                        "traditional_names": traditional_names,
                        "active_compounds": active_compounds,
                        "safety_caution": safety_caution
                    }
                )


            
                       # ==================================================
            # HERB–DRUG INTERACTION SCREENING
            # ==================================================

            interaction_findings = []


            if not selected_herb_data.empty:

                for _, herb_row in selected_herb_data.iterrows():

                    herb_name = herb_row["Herb"]

                    interaction_class = (
                        herb_row["Interaction_Class"]
                    )

                    active_compounds = (
                        herb_row["Active_Compounds"]
                    )

                    scientific_name = (
                        herb_row["Scientific"]
                    )


                    if pd.isna(interaction_class):
                        interaction_class = ""

                    if pd.isna(active_compounds):
                        active_compounds = "Not available"

                    if pd.isna(scientific_name):
                        scientific_name = "Not available"


                    interaction_class = str(
                        interaction_class
                    ).strip()


                    if not interaction_class:
                        continue


                    herb_interactions = interactions_df[
                        interactions_df["Herb"].astype(str).str.strip()
                        == str(herb_name).strip()
                    ]


                    for _, interaction in herb_interactions.iterrows():

                        drug_class = str(
                            interaction["Drug_Class"]
                        ).strip()


                        risk = str(
                            interaction["Risk"]
                        ).strip()


                        # ------------------------------------------
                        # SAFE EVIDENCE NOTE
                        # ------------------------------------------

                        evidence = interaction.get(
                            "Evidence_Note",
                            interaction.get(
                                "Evidence",
                                "Structured interaction information from the SmartRx AI database."
                            )
                        )


                        if pd.isna(evidence):
                            evidence = (
                                "Structured interaction information "
                                "from the SmartRx AI database."
                            )


                        affected_medicines = chosen[
                            chosen["Category"]
                            .astype(str)
                            .str.strip()
                            .str.upper()
                            .eq(drug_class.upper())
                        ]


                        if not affected_medicines.empty:

                            interaction_findings.append(
                                {
                                    "herb": herb_name,

                                    "drug_class": drug_class,

                                    "medicines":
                                        affected_medicines[
                                            "Medicine"
                                        ].tolist(),

                                    "scientific_name":
                                        scientific_name,

                                    "active_compounds":
                                        active_compounds,

                                    "risk":
                                        risk,

                                    "evidence":
                                        str(evidence)
                                }
                            )
            # ==================================================
            # DISPLAY HERB–DRUG INTERACTIONS
            # ==================================================

            if interaction_findings:

                st.subheader(
                    "🚨 Potential Herb–Drug Interactions"
                )


                for item in interaction_findings:

                    if item["risk"].lower() == "high":
                        border = "#DC2626"

                    elif item["risk"].lower() == "moderate":
                        border = "#F59E0B"

                    else:
                        border = "#16A34A"


                    st.markdown(
                        f"""
                        <div style="
                            background:white;
                            border-left:8px solid {border};
                            padding:20px;
                            border-radius:15px;
                            margin-bottom:18px;
                            box-shadow:
                            0 4px 12px rgba(0,0,0,0.08);
                        ">

                        <h4 style="color:{border};">
                        🚨 {item["herb"]} +
                        {item["drug_class"]} Medicines
                        </h4>

                        <p>
                        <strong>Orthodox Medicines:</strong>
                        {", ".join(item["medicines"])}
                        </p>

                        <p>
                        <strong>Scientific Name:</strong>
                        <em>{item["scientific_name"]}</em>
                        </p>

                        <p>
                        <strong>Major Active Compounds:</strong>
                        {item["active_compounds"]}
                        </p>

                        <p>
                        <strong>Risk Level:</strong>
                        {item["risk"]}
                        </p>

                        <p>
                        <strong>Evidence Note:</strong>
                        {item["evidence"]}
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


            # ==================================================
            # NO MAJOR RULE-BASED ISSUE
            # ==================================================

            if (
                not duplicates
                and not category_warnings
                and not interaction_findings
            ):

                st.markdown(
                    """
                    <div class="safe">

                    <h3>
                    ✅ No Major Issue Detected by Current Rules
                    </h3>

                    <p>
                    No duplicate active ingredients,
                    multiple-NSAID conflicts or stored
                    herb–drug interaction flags were
                    identified by the current structured
                    screening rules.
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ==================================================
            # STRUCTURED SMART RX AI FINDINGS
            # ==================================================

            safety_findings = {

                "selected_medicines":
                    selected_medicines,

                "duplicate_active_ingredients":
                    duplicate_details,

                "category_warnings":
                    category_warnings,

                "medicine_warnings":
                    medicine_warnings,

                "herb_drug_interactions":
                    interaction_findings,

                "selected_herbs":
                    herbal_findings
            }


            # ==================================================
            # AI SAFETY EXPLANATION
            # ==================================================

            st.subheader(
                "🤖 AI Safety Explanation"
            )


            with st.spinner(
                "SmartRx AI is generating a safety explanation..."
            ):

                try:

                    ai_explanation = (
                        generate_ai_explanation(
                            safety_findings
                        )
                    )

                except Exception:

                    ai_explanation = (
                        "The structured safety screening was "
                        "completed, but the AI explanation "
                        "could not be generated at this time."
                    )

                    st.warning(
                        "AI explanation service is temporarily "
                        "unavailable. The structured screening "
                        "results above are still available."
                    )


            st.markdown(
                """
                <div class="ai-box">

                <h3 style="color:#4338CA;">
                🤖 Meta AI Safety Explanation
                </h3>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.write(ai_explanation)


            # ==================================================
            # DISCLAIMER
            # ==================================================

            st.info(
                "⚠️ SmartRx AI provides educational and "
                "decision-support information only. It does "
                "not diagnose medical conditions or replace "
                "a qualified doctor or pharmacist."
            )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">

    <strong>SmartRx AI © 2026</strong><br>

    AI-Powered Medication & Herbal Safety Intelligence<br>

    Developed by Chizix Orbit Digital Innovations Ltd. 🇳🇬

    </div>
    """,
    unsafe_allow_html=True
)
