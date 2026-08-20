import streamlit as st
import pandas as pd

# ==========================================================
# LOAD MEDICATION DATABASE
# ==========================================================

try:
    medicines_df = pd.read_csv("medicines.csv")
except FileNotFoundError:
    st.error("medicines.csv not found. Please make sure it is in the same repository folder as app.py.")
    st.stop()

medicine_list = sorted(
    medicines_df["Medicine"].dropna().unique().tolist()
)

# ==========================================================
# SMART RX AI — PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="SmartRx AI",
    page_icon="💊",
    layout="wide"
)

# ==========================================================
# SMART RX AI — CUSTOM STYLING
# ==========================================================

st.markdown("""
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
   INDIGO SMART RX AI HERO
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
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.20);
}

/* ======================================================
   GENERAL CARDS
   ====================================================== */

.card {
    background: #FFFFFF;
    border: 1px solid rgba(20,70,124,0.10);
    box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
}

/* ======================================================
   SAFETY RESULT BOXES
   ====================================================== */

.safe {
    background-color: #D1FAE5;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid green;
    margin-bottom: 15px;
}

.warning {
    background-color: #FEF3C7;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid orange;
    margin-bottom: 15px;
}

.danger {
    background-color: #FEE2E2;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid red;
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
}

/* ======================================================
   SECTION BOX
   ====================================================== */

.section {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(20,70,124,0.10);
    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* ======================================================
   HEADINGS
   ====================================================== */

h1, h2, h3, h4 {
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
""", unsafe_allow_html=True)


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

    st.markdown("""
    <div class="hero">

        <h1 style="color:white;">
        💊 SmartRx AI
        </h1>

        <h3 style="color:white;">
        AI-Powered Medication & Herbal Safety Intelligence
        </h3>

        <p>
        SmartRx AI is an intelligent medication-safety platform
        designed to help users understand potential risks involving
        orthodox medicines, traditional African medicinal herbs,
        duplicate active ingredients and medication combinations.
        </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="card">

        <h3>💊 Medication Intelligence</h3>

        <p>
        Analyse multiple medicines and identify duplicate
        active ingredients and potential medication conflicts.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">

        <h3>🌿 Herbal Intelligence</h3>

        <p>
        Cross-reference Nigerian traditional medicinal herbs
        with pharmaceutical medicines using an ethnobotanical
        safety knowledge base.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="card">

        <h3>🤖 Meta AI Intelligence</h3>

        <p>
        Use Meta AI intelligence to generate explainable safety
        summaries from structured medication and herbal screening results.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
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
    """, unsafe_allow_html=True)


# ==========================================================
# ABOUT PAGE
# ==========================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About SmartRx AI")

    st.markdown("""
    <div class="section">

    <h2 style="color:#4338CA;">
    The Innovation
    </h2>

    <p>
    <strong>SmartRx AI</strong> is an AI-powered medication and
    herbal safety intelligence platform developed by
    <strong>Chizix Orbit Digital Innovations Ltd.</strong>
    </p>

    <p>
    The platform is designed to bridge pharmaceutical medication
    information with Traditional African Medicine by combining
    structured safety knowledge with artificial intelligence.
    </p>

    <p>
    SmartRx AI is designed to use <strong>Meta AI models</strong>
    as an AI intelligence and explanation layer, helping transform
    structured safety findings into understandable information
    for users.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">

    <h3 style="color:#4338CA;">
    Core Capabilities
    </h3>

    <p>💊 Orthodox medicine intelligence</p>
    <p>🌿 Nigerian herbal medicine intelligence</p>
    <p>🔬 Active ingredient analysis</p>
    <p>⚠️ Medication duplication screening</p>
    <p>🌿 Herb–drug safety screening</p>
    <p>🤖 Meta AI-powered explanations</p>
    <p>🇳🇬 Nigerian-focused health innovation</p>

    </div>
    """, unsafe_allow_html=True)

    st.info(
        "SmartRx AI is an educational and decision-support platform. "
        "It does not replace a qualified doctor, pharmacist or other "
        "healthcare professional."
    )


# ==========================================================
# HOW TO USE PAGE
# ==========================================================

elif page == "📘 How To Use":

    st.title("📘 How To Use SmartRx AI")

    steps = [
        (
            "Step 1 — Select Your Medicines",
            "Go to AI Safety Checker and select all the orthodox "
            "medicines you are currently taking."
        ),
        (
            "Step 2 — Select Your Herbs",
            "Select up to four Nigerian or Traditional African "
            "medicinal herbs from the herb dropdowns."
        ),
        (
            "Step 3 — Run Safety Screening",
            "Click the AI Safety Verification button to analyse "
            "the selected medicines and herbs."
        ),
        (
            "Step 4 — Review Structured Findings",
            "SmartRx AI checks for duplicate active ingredients, "
            "medicine-class conflicts and potential herb–drug "
            "safety concerns."
        ),
        (
            "Step 5 — Read the AI Explanation",
            "The Meta AI layer will explain the structured "
            "findings in clearer, user-friendly language."
        ),
        (
            "Step 6 — Seek Professional Advice",
            "Use the results as safety information and consult a "
            "qualified healthcare professional before making "
            "medication decisions."
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

    st.markdown("""
    <div class="section">

    <h3 style="color:#4338CA;">
    Medication & Herbal Safety Verification
    </h3>

    <p>
    Select the medicines and herbs you want SmartRx AI to analyse.
    The complete safety engine will compare the selected items and
    generate an explainable safety report.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.info(
        "🚧 The medication and Nigerian herbal knowledge bases "
        "are being loaded into this version of SmartRx AI."
    )

    st.markdown("""
    <div class="ai-box">

    <h3 style="color:#4338CA;">
    🤖 Meta AI Intelligence Layer
    </h3>

    <p>
    SmartRx AI will use Meta AI intelligence to transform structured
    medication-safety findings into clear, explainable summaries.
    </p>

    <p>
    The AI layer will be connected securely through Streamlit
    Secrets. API credentials will never be stored in this repository.
    </p>

    </div>
    """, unsafe_allow_html=True)


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
