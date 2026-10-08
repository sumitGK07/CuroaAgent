import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai

from research.router import route_query
from research.search import search_medical


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# GEMINI CLIENT
# =========================================================

client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CuroaAgent",
    page_icon="🩺",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #888888;
        margin-bottom: 30px;
    }

    .doctor-box {
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 15px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🩺 CuroaAgent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI Digital Doctor & Health Research Agent'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "💬 Describe your health problem in your own words. "
    "CuroaAgent intelligently selects the most useful "
    "medical research source and explains the information."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🩺 CuroaAgent")

    st.write("Your Digital Doctor")

    st.divider()

    st.subheader("I can help with")

    st.write("🤒 Fever")
    st.write("🤧 Cold")
    st.write("😷 Cough")
    st.write("🤕 Headache")
    st.write("🫃 Stomach problems")
    st.write("🦠 Infection-related questions")
    st.write("🌸 Allergies")
    st.write("🩹 Skin problems")
    st.write("💪 Body pain")
    st.write("📋 General health questions")

    st.divider()

    st.subheader("🧠 Research Engines")

    st.write("🔎 Google Search")
    st.write("📚 Google Scholar")
    st.write("📰 Google News")

    st.divider()

    st.caption(
        "⚠️ CuroaAgent provides health information "
        "and does not replace a qualified healthcare professional."
    )


# =========================================================
# USER HEALTH QUESTION
# =========================================================

st.subheader("💬 Tell me what you're experiencing")

query = st.text_area(
    "Describe your symptoms or health concern",
    placeholder=(
        "Example:\n"
        "I have fever, sore throat and cough for 2 days. "
        "What could be causing it?"
    ),
    height=140
)


# =========================================================
# RESEARCH MODE
# =========================================================

st.subheader("🧠 Research Mode")

research_mode = st.selectbox(
    "How should CuroaAgent research your question?",
    [
        "Auto (Recommended)",
        "General Medical Search",
        "Medical Research / Studies",
        "Latest Medical News"
    ]
)


# =========================================================
# QUICK QUESTIONS
# =========================================================

st.write("**Quick questions:**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    fever_button = st.button("🤒 Fever")

with col2:
    cold_button = st.button("🤧 Cold")

with col3:
    cough_button = st.button("😷 Cough")

with col4:
    headache_button = st.button("🤕 Headache")


if fever_button:
    query = (
        "I have a fever. What could be the possible causes, "
        "what symptoms should I watch for, and when should "
        "I see a doctor?"
    )

if cold_button:
    query = (
        "I have cold symptoms. What could be causing them, "
        "what can I generally do, and when should I see a doctor?"
    )

if cough_button:
    query = (
        "I have a cough. What are the possible causes, "
        "what should I watch for, and when should I see a doctor?"
    )

if headache_button:
    query = (
        "I have a headache. What are the possible causes, "
        "what can I generally do, and when should I seek "
        "medical help?"
    )


# =========================================================
# ASK CUROAAGENT
# =========================================================

if st.button(
    "🩺 Ask CuroaAgent",
    type="primary"
):

    # =====================================================
    # CHECK GEMINI KEY
    # =====================================================

    if not GEMINI_API_KEY:

        st.error(
            "❌ Gemini API key not found. "
            "Check your .env file."
        )

        st.stop()


    # =====================================================
    # CHECK QUESTION
    # =====================================================

    if not query.strip():

        st.warning(
            "⚠️ Please describe your health problem first."
        )

        st.stop()


    # =====================================================
    # STEP 1 — INTELLIGENT RESEARCH ROUTING
    # =====================================================

    with st.status(
        "🧠 CuroaAgent is planning the research...",
        expanded=True
    ) as research_status:

        st.write(
            "🔍 Understanding your question..."
        )


        # -------------------------------------------------
        # AUTO MODE
        # -------------------------------------------------

        if research_mode == "Auto (Recommended)":

            research_plan = route_query(query)


        # -------------------------------------------------
        # MANUAL GOOGLE
        # -------------------------------------------------

        elif research_mode == "General Medical Search":

            research_plan = {
                "engine": "google",
                "research_type": "General Medical Search",
                "reason": (
                    "General medical information search "
                    "was selected."
                )
            }


        # -------------------------------------------------
        # MANUAL SCHOLAR
        # -------------------------------------------------

        elif research_mode == "Medical Research / Studies":

            research_plan = {
                "engine": "google_scholar",
                "research_type": "Medical Research",
                "reason": (
                    "Scientific research and academic "
                    "evidence search was selected."
                )
            }


        # -------------------------------------------------
        # MANUAL NEWS
        # -------------------------------------------------

        else:

            research_plan = {
                "engine": "google_news",
                "research_type": "Latest Medical News",
                "reason": (
                    "Recent medical news search "
                    "was selected."
                )
            }


        st.write(
            f"🎯 Research type: "
            f"**{research_plan['research_type']}**"
        )

        st.write(
            f"🔎 Search engine: "
            f"**{research_plan['engine']}**"
        )

        st.write(
            f"💡 Reason: "
            f"{research_plan['reason']}"
        )


        research_status.update(
            label="🎯 Research plan ready!",
            state="complete",
            expanded=False
        )


    # =====================================================
    # STEP 2 — SERPAPI RESEARCH
    # =====================================================

    with st.status(
        "🔎 CuroaAgent is researching...",
        expanded=True
    ) as search_status:

        st.write(
            "🌐 Connecting to SerpApi..."
        )

        st.write(
            f"🔎 Searching with "
            f"**{research_plan['engine']}**..."
        )


        search_result = search_medical(
            query,
            research_plan["engine"]
        )


        # -------------------------------------------------
        # SEARCH FAILED
        # -------------------------------------------------

        if not search_result["success"]:

            search_status.update(
                label="❌ Research failed",
                state="error",
                expanded=True
            )

            st.error(
                search_result["error"]
            )

            st.stop()


        results = search_result["results"]


        st.write(
            f"📚 Found {len(results)} research sources."
        )


        search_status.update(
            label="📚 Medical research completed!",
            state="complete",
            expanded=False
        )


    # =====================================================
    # STEP 3 — PREPARE RESEARCH FOR GEMINI
    # =====================================================

    research_text = ""


    # Only send maximum 3 sources to Gemini.
    # This keeps the prompt smaller and faster.

    for i, result in enumerate(
        results[:3],
        start=1
    ):

        title = result.get(
            "title",
            "Unknown source"
        )

        source = result.get(
            "source",
            ""
        )

        snippet = result.get(
            "snippet",
            ""
        )

        link = result.get(
            "link",
            ""
        )


        # Limit each snippet
        snippet = snippet[:800]


        research_text += f"""

SOURCE {i}

Title:
{title}

Source:
{source}

Information:
{snippet}

Link:
{link}

"""


    # =====================================================
    # STEP 4 — DIGITAL DOCTOR PROMPT
    # =====================================================

    prompt = f"""
You are CuroaAgent, a Digital Doctor and AI health
information assistant.

The user asked:

{query}


RESEARCH METHOD SELECTED:

{research_plan['research_type']}


SERPAPI SEARCH ENGINE:

{research_plan['engine']}


LIVE MEDICAL RESEARCH:

{research_text}


YOUR TASK:

Analyze the user's health concern using the research
provided above.

Give a useful, detailed but easy-to-understand response.

IMPORTANT SAFETY RULES:

1. Do NOT diagnose the user.
2. Do NOT say the user definitely has a disease.
3. Do NOT promise a cure.
4. Do NOT invent medical facts.
5. Clearly describe possibilities rather than confirmed diagnoses.
6. Provide general health guidance when appropriate.
7. Explain important symptoms to monitor.
8. Explain when professional medical evaluation is recommended.
9. If symptoms could indicate an emergency, clearly recommend
   urgent medical attention.
10. Do not discourage professional medical care.
11. If the research is uncertain or conflicting, say so.
12. Do not present news reports as established medical evidence.

For scientific/research questions:

Explain what the available research suggests and clearly
distinguish evidence from uncertainty.

For recent/news questions:

Clearly explain that recent medical developments
can change over time.


USE THIS STRUCTURE:

## 🩺 What I understand

Briefly explain the user's concern.

## 🔍 Possible explanations

Explain relevant possible causes or explanations.
Do not present them as confirmed diagnoses.

## 📚 What the research says

Summarize the most useful information from the
retrieved research.

## 💡 General guidance

Give safe and general guidance when appropriate.

## ⚠️ When to see a doctor

Explain when professional medical evaluation
is recommended.

## 🚨 Seek urgent help if

Mention relevant emergency warning signs.

Use simple language that a normal person can understand.

End with:

"This information is for educational purposes and is not
a medical diagnosis."
"""


    # =====================================================
    # STEP 5 — GEMINI ANALYSIS
    # =====================================================

    with st.status(
        "🧠 CuroaAgent is analyzing the research...",
        expanded=True
    ) as ai_status:

        st.write(
            "📖 Reading retrieved medical information..."
        )

        st.write(
            "🧠 Gemini is analyzing the evidence..."
        )


        answer = None
        successful_model = None


        # -------------------------------------------------
        # GEMINI MODEL
        # -------------------------------------------------

        models_to_try = [
            "gemini-3.8-flash"
        ]


        # -------------------------------------------------
        # TRY GEMINI
        # -------------------------------------------------

        for model_name in models_to_try:

            for attempt in range(2):

                try:

                    gemini_response = (
                        client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config={
                                "temperature": 0.2,
                                "max_output_tokens": 1200
                            }
                        )
                    )


                    answer = gemini_response.text

                    successful_model = model_name

                    break


                except Exception as e:

                    error_text = str(e)


                    # PRINT COMPLETE ERROR
                    # TO POWERSHELL

                    print(
                        "\n"
                        "==========================================\n"
                        "           GEMINI API ERROR\n"
                        "=========================================="
                    )

                    print(error_text)

                    print(
                        "==========================================\n"
                    )


                    # -------------------------------------------------
                    # TEMPORARY SERVER ERROR
                    # -------------------------------------------------

                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                    ):

                        if attempt < 1:

                            print(
                                "Gemini temporarily unavailable."
                            )

                            print(
                                "Retrying in 2 seconds..."
                            )

                            time.sleep(2)

                            continue


                    break


            if answer:

                break


    # =====================================================
    # GEMINI FAILED
    # =====================================================

    if not answer:

        ai_status.update(
            label="❌ Gemini analysis failed",
            state="error",
            expanded=True
        )

        st.error(
            "❌ Gemini could not generate the response."
        )

        st.info(
            "The detailed Gemini error has been printed "
            "in your PowerShell / terminal window."
        )

        st.stop()


    # =====================================================
    # SUCCESS
    # =====================================================

    ai_status.update(
        label="🩺 Analysis completed!",
        state="complete",
        expanded=False
    )


    # =====================================================
    # DISPLAY AI RESPONSE
    # =====================================================

    st.divider()

    st.subheader(
        "🩺 CuroaAgent Analysis"
    )


    st.markdown(
        '<div class="doctor-box">',
        unsafe_allow_html=True
    )


    st.markdown(answer)


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # SOURCES
    # =====================================================

    st.divider()

    st.subheader(
        "📚 Medical Research Sources"
    )


    st.caption(
        f"Research source selected: "
        f"{research_plan['research_type']}"
    )


    for i, result in enumerate(
        results[:5],
        start=1
    ):

        title = result.get(
            "title",
            "Medical source"
        )

        link = result.get(
            "link",
            ""
        )

        snippet = result.get(
            "snippet",
            ""
        )

        source = result.get(
            "source",
            ""
        )


        with st.expander(
            f"🔗 {i}. {title}"
        ):

            if source:

                st.write(
                    f"**Source:** {source}"
                )


            st.write(
                snippet
            )


            if link:

                st.link_button(
                    "Read Source",
                    link
                )


    # =====================================================
    # TECHNICAL DETAILS
    # =====================================================

    with st.expander(
        "⚙️ CuroaAgent Agent Details"
    ):

        st.write(
            f"Research type: "
            f"{research_plan['research_type']}"
        )

        st.write(
            f"SerpApi engine: "
            f"{research_plan['engine']}"
        )

        st.write(
            f"Sources retrieved: "
            f"{len(results)}"
        )

        st.write(
            f"Gemini model: "
            f"{successful_model}"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🩺 CuroaAgent — AI-powered Digital Doctor"
)

st.caption(
    "⚠️ For educational purposes only. "
    "Always consult a qualified healthcare professional "
    "for diagnosis and treatment."
)