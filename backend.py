# =========================================================
# CUROAAGENT - BACKEND
# =========================================================

import os
import re

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from research.router import route_query
from research.search import search_medical


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

app = Flask(__name__)
CORS(app)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "agent": "CuroaAgent",
        "status": "online"
    })


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# CREATE MEDICAL ANSWER
# =========================================================

def create_research_answer(query, results, research_type):

    if not results:
        return """
        <h2>🩺 Let's look at your symptoms</h2>

        <p>
            I couldn't find enough reliable medical information
            to give you a useful research-based answer right now.
        </p>

        <p>
            If your fever has been continuing for several days,
            especially if it is getting worse or you have other
            concerning symptoms, please contact a healthcare
            professional for an evaluation.
        </p>
        """


    # =====================================================
    # COLLECT RESEARCH SNIPPETS
    # =====================================================

    snippets = []

    for result in results:

        snippet = clean_text(
            result.get("snippet", "")
        )

        if snippet:
            snippets.append(snippet)


    combined_text = " ".join(snippets)

    lower_text = combined_text.lower()


    # =====================================================
    # POSSIBLE CAUSES
    # =====================================================

    possible_causes = []


    cause_keywords = [

        (
            "viral",
            "Viral infections are a common reason for fever. They can occur with symptoms such as cough, sore throat, tiredness, headache, body aches, chills, or congestion."
        ),

        (
            "flu",
            "Influenza (flu) can cause fever along with chills, body aches, headache, tiredness, cough, and other respiratory symptoms."
        ),

        (
            "covid",
            "COVID-19 can cause fever and may occur with cough, sore throat, tiredness, headache, body aches, or other respiratory symptoms."
        ),

        (
            "bacterial",
            "Some bacterial infections can cause persistent fever. The symptoms and treatment depend on where the infection is located and what organism is responsible."
        ),

        (
            "respiratory",
            "Respiratory infections can cause fever together with cough, sore throat, congestion, breathing symptoms, or chest discomfort."
        ),

        (
            "urinary",
            "A urinary tract infection can sometimes cause fever. If the infection involves the kidneys, symptoms may include fever, chills, back or side pain, or painful urination."
        ),

        (
            "inflammation",
            "Some inflammatory conditions can also cause fever. These cannot be identified from fever alone and may require a medical examination."
        )

    ]


    for keyword, explanation in cause_keywords:

        if keyword in lower_text:

            possible_causes.append(
                explanation
            )


    # Remove duplicates
    unique_causes = []

    for cause in possible_causes:

        if cause not in unique_causes:

            unique_causes.append(cause)


    # Limit causes
    unique_causes = unique_causes[:5]


    # =====================================================
    # FALLBACK CAUSES
    # =====================================================

    if not unique_causes:

        unique_causes = [

            "Infections are one of the most common reasons for fever, including viral and bacterial infections.",

            "The source of a fever can sometimes be outside the respiratory system, so symptoms such as urinary problems, abdominal pain, rash, or other changes are important to mention to a healthcare professional.",

            "Other less common conditions can also cause persistent fever, which is why the duration of the fever and the other symptoms you have are important."
        ]


    # =====================================================
    # CREATE POSSIBLE CAUSES HTML
    # =====================================================

    causes_html = ""


    for index, cause in enumerate(
        unique_causes,
        start=1
    ):

        causes_html += f"""

        <div class="medical-section">

            <h3>
                {index}. Possible cause
            </h3>

            <p>
                {cause}
            </p>

        </div>

        """


    # =====================================================
    # DETAILED ANSWER
    # =====================================================

    answer = f"""

    <h2>
        🩺 Fever for 5 Days — What You Should Know
    </h2>


    <p>
        You told me:
        <strong>{query}</strong>
    </p>


    <p>
        A fever that has continued for around five days
        deserves medical attention rather than simply being
        watched indefinitely. Fever itself is a symptom, not
        a diagnosis, and there are many possible reasons for
        it. The other symptoms you have, your temperature,
        medical history, medications, and physical examination
        all help determine the likely cause.
    </p>


    <div class="warning-box">

        <strong>
            ⚠️ Important: Your fever has lasted 5 days
        </strong>

        <p>
            Because the fever has continued for five days,
            it would be sensible to arrange an evaluation with
            a healthcare professional, particularly if the
            fever is still present, keeps returning, is getting
            worse, or you are feeling increasingly unwell.
        </p>

    </div>


    <h3>
        🌡️ First, check your temperature
    </h3>


    <p>
        If possible, use a digital thermometer and keep track
        of your temperature. Write down the highest temperature
        you have measured and when you measured it.
    </p>


    <p>
        Also note whether the fever comes and goes or remains
        continuously elevated. This information can be useful
        when you speak with a doctor.
    </p>


    <h3>
        🔎 What could be causing the fever?
    </h3>


    <p>
        Fever can happen when the body is responding to an
        infection or another condition. Common possibilities
        include viral infections, influenza, respiratory
        infections, and some bacterial infections. However,
        fever alone is not enough to determine which condition
        you have.
    </p>


    {causes_html}


    <h3>
        🧩 Your other symptoms are very important
    </h3>


    <p>
        The next thing to consider is what other symptoms you
        have along with the fever. Tell a healthcare professional
        if you have any of the following:
    </p>


    <div class="medical-section">

        <h3>
            🤧 Respiratory symptoms
        </h3>

        <p>
            Cough, sore throat, runny or blocked nose,
            shortness of breath, wheezing, or chest discomfort
            may provide clues about a respiratory infection.
        </p>

    </div>


    <div class="medical-section">

        <h3>
            🤕 Head and neurological symptoms
        </h3>

        <p>
            Headache, unusual drowsiness, confusion, severe
            weakness, sensitivity to light, or a stiff neck
            are important symptoms that should not be ignored.
        </p>

    </div>


    <div class="medical-section">

        <h3>
            🤢 Stomach and digestive symptoms
        </h3>

        <p>
            Abdominal pain, repeated vomiting, diarrhea,
            inability to drink fluids, or significant loss
            of appetite should be mentioned when seeking care.
        </p>

    </div>


    <div class="medical-section">

        <h3>
            🚽 Urinary symptoms
        </h3>

        <p>
            Pain or burning when urinating, needing to urinate
            frequently, blood in the urine, or pain in your
            back or side can be relevant when investigating
            a fever.
        </p>

    </div>


    <div class="medical-section">

        <h3>
            🩹 Skin symptoms
        </h3>

        <p>
            A new rash, unusual skin changes, or a rapidly
            worsening rash should be reported to a healthcare
            professional.
        </p>

    </div>


    <h3>
        💧 Keep yourself hydrated
    </h3>


    <p>
        Fever can increase fluid loss, particularly if you are
        sweating, vomiting, or having diarrhea. Drink fluids
        regularly and pay attention to signs of dehydration.
    </p>


    <p>
        Signs that you may be becoming dehydrated can include
        a very dry mouth, dark urine, urinating less than usual,
        dizziness, unusual tiredness, or difficulty keeping
        fluids down.
    </p>


    <h3>
        🛌 What you can do while arranging medical advice
    </h3>


    <p>
        Get adequate rest and drink enough fluids. Keep track
        of your temperature and note any new symptoms.
        Avoid strenuous activity while you are feeling unwell.
    </p>


    <p>
        If you normally take an over-the-counter medicine for
        fever or pain, follow the product label carefully.
        If you have other medical conditions, take regular
        medicines, are pregnant, or are unsure whether a
        medicine is appropriate for you, ask a doctor or
        pharmacist before taking it.
    </p>


    <div class="warning-box">

        <strong>
            🚨 Get urgent medical help if you develop:
        </strong>

        <p>
            Difficulty breathing, severe or persistent chest
            pain, confusion, fainting, a seizure, a severe
            headache with a stiff neck, repeated vomiting,
            severe dehydration, difficulty swallowing fluids,
            severe abdominal pain, a rapidly spreading or
            concerning rash, or a rapidly worsening condition.
        </p>

    </div>


    <h3>
        🏥 What might a healthcare professional check?
    </h3>


    <p>
        A healthcare professional may ask how long you have
        had the fever, how high your temperature has been,
        whether it comes and goes, and what other symptoms
        you have.
    </p>


    <p>
        Depending on your symptoms and examination, they may
        decide that you need additional tests. These could
        include blood tests, urine testing, respiratory tests,
        or imaging such as a chest X-ray when appropriate.
        The specific tests depend on your symptoms and medical
        history rather than simply the number of days of fever.
    </p>


    <h3>
        📝 Information to prepare before your appointment
    </h3>


    <p>
        It can help to note:
    </p>


    <div class="medical-section">

        <p>
            • Your highest measured temperature<br>
            • When the fever started<br>
            • Whether the fever is continuous or comes and goes<br>
            • Any medicines you have taken and their doses<br>
            • Cough, sore throat, headache, body aches or chills<br>
            • Vomiting or diarrhea<br>
            • Abdominal or urinary symptoms<br>
            • Any rash or skin changes<br>
            • Any recent travel or contact with someone who was ill
        </p>

    </div>


    <h3>
        💬 A few questions that would help me understand your situation
    </h3>


    <p>
        If you want, tell me:
    </p>


    <div class="medical-section">

        <p>
            <strong>1.</strong> What is your highest temperature
            in °C or °F?<br><br>

            <strong>2.</strong> Is the fever continuous or does
            it come and go?<br><br>

            <strong>3.</strong> Do you have cough, sore throat,
            headache, body pain, chills, vomiting, diarrhea,
            stomach pain, or urinary symptoms?<br><br>

            <strong>4.</strong> Do you have any rash or unusual
            skin changes?<br><br>

            <strong>5.</strong> What medicines have you taken
            for the fever?<br><br>

            <strong>6.</strong> Are you able to drink fluids
            and urinate normally?
        </p>

    </div>


    <p>
        These details can help CuroaAgent give you more
        relevant general information, but they cannot replace
        an examination by a qualified healthcare professional.
    </p>


    <p>
        <strong>
            CuroaAgent does not diagnose the cause of your
            fever or prescribe treatment.
        </strong>
        If your five-day fever is still present, arranging
        medical evaluation is the safest next step.
    </p>

    """


    return answer


    # -----------------------------------------------------
    # Collect snippets from SerpApi
    # -----------------------------------------------------

    snippets = []

    for result in results:

        snippet = clean_text(
            result.get("snippet", "")
        )

        if snippet:
            snippets.append(snippet)


    combined_text = " ".join(snippets)

    lower_text = combined_text.lower()


    # -----------------------------------------------------
    # Possible causes
    # -----------------------------------------------------

    possible_causes = []


    cause_keywords = [

        (
            "viral infection",
            "A viral infection can cause fever and may occur with symptoms such as tiredness, cough, sore throat, or body aches."
        ),

        (
            "bacterial infection",
            "Some bacterial infections can cause persistent fever and may require medical evaluation."
        ),

        (
            "respiratory infection",
            "Respiratory infections can cause fever together with symptoms such as cough, congestion, or sore throat."
        ),

        (
            "flu",
            "Influenza can cause fever and may also cause body aches, tiredness, cough, chills, and headache."
        ),

        (
            "covid",
            "COVID-19 can cause fever along with respiratory or other symptoms."
        ),

        (
            "urinary",
            "A urinary tract infection can sometimes cause fever, particularly when the infection affects the kidneys."
        ),

        (
            "inflammation",
            "Some inflammatory conditions can also be associated with persistent fever."
        )

    ]


    # -----------------------------------------------------
    # Find possible causes in research
    # -----------------------------------------------------

    for keyword, explanation in cause_keywords:

        if keyword in lower_text:

            possible_causes.append(
                explanation
            )


    # -----------------------------------------------------
    # If no keywords were found
    # -----------------------------------------------------

    if not possible_causes:

        for snippet in snippets[:3]:

            if snippet not in possible_causes:

                possible_causes.append(
                    snippet
                )


    # Remove duplicates

    unique_causes = []

    for cause in possible_causes:

        if cause not in unique_causes:

            unique_causes.append(cause)


    # Maximum 4 causes

    unique_causes = unique_causes[:4]


    # -----------------------------------------------------
    # Create cause HTML
    # -----------------------------------------------------

    causes_html = ""


    for index, cause in enumerate(
        unique_causes,
        start=1
    ):

        causes_html += f"""
        <div class="medical-section">

            <h3>
                {index}. Possible explanation
            </h3>

            <p>
                {cause}
            </p>

        </div>
        """


    # -----------------------------------------------------
    # Main answer
    # -----------------------------------------------------

    answer = f"""
    <h2>
        🩺 What could be causing this?
    </h2>


    <p>
        You mentioned:
        <strong>{query}</strong>
    </p>


    <p>
        A fever that has lasted around five days
        is worth paying attention to. Fever can occur
        with several different infections and other
        conditions, and the cause cannot be determined
        from this information alone.
    </p>


    <h3>
        🔎 Possible causes
    </h3>


    {causes_html}


    <div class="warning-box">

        <strong>
            ⚠️ Because your fever has lasted 5 days
        </strong>

        <p>
            Consider contacting a healthcare professional
            for an evaluation, especially if the fever is
            persistent, getting worse, or accompanied by
            other concerning symptoms.
        </p>

    </div>


    <h3>
        👀 Watch for these symptoms
    </h3>


    <p>
        Seek urgent medical attention if you develop
        difficulty breathing, severe chest pain,
        confusion, fainting, a seizure, a severe headache
        or stiff neck, severe dehydration, or a rapidly
        worsening condition.
    </p>


    <p>
        CuroaAgent provides general educational
        information and cannot diagnose the cause of
        your fever.
    </p>
    """


    return answer


# =========================================================
# CHAT API
# =========================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        # -------------------------------------------------
        # Get request
        # -------------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({
                "success": False,
                "error": "No request data received."
            }), 400


        # -------------------------------------------------
        # Get question
        # -------------------------------------------------

        query = data.get(
            "message",
            ""
        ).strip()


        if not query:

            return jsonify({
                "success": False,
                "error": "Please enter a health question."
            }), 400


        # -------------------------------------------------
        # Get selected research engine
        # -------------------------------------------------

        requested_engine = data.get(
            "engine",
            "auto"
        )


        # -------------------------------------------------
        # Auto research
        # -------------------------------------------------

        if requested_engine == "auto":

            research_plan = route_query(
                query
            )


        # -------------------------------------------------
        # Manual research selection
        # -------------------------------------------------

        else:

            engine_map = {

                "google": {
                    "engine": "google",
                    "research_type": "General Medical Search",
                    "reason": "General medical information search."
                },

                "google_scholar": {
                    "engine": "google_scholar",
                    "research_type": "Medical Studies",
                    "reason": "Searching academic medical research and studies."
                },

                "google_news": {
                    "engine": "google_news",
                    "research_type": "Latest Medical News",
                    "reason": "Searching recent medical news and developments."
                }

            }


            research_plan = engine_map.get(
                requested_engine,
                engine_map["google"]
            )


        # -------------------------------------------------
        # Console information
        # -------------------------------------------------

        print()
        print("==========================================")
        print("CUROAAGENT")
        print("==========================================")

        print(
            f"Question: {query}"
        )

        print(
            f"Research: {research_plan['research_type']}"
        )

        print(
            f"Engine: {research_plan['engine']}"
        )

        print(
            "Searching SerpApi..."
        )


        # -------------------------------------------------
        # Search SerpApi
        # -------------------------------------------------

        search_result = search_medical(
            query,
            research_plan["engine"]
        )


        if not search_result["success"]:

            return jsonify({
                "success": False,
                "error": search_result["error"]
            }), 500


        results = search_result["results"]


        print(
            f"Found {len(results)} sources."
        )


        # -------------------------------------------------
        # Generate conversational answer
        # -------------------------------------------------

        answer = create_research_answer(
            query,
            results,
            research_plan["research_type"]
        )


        # -------------------------------------------------
        # Send response
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "answer": answer,

            "ai_analysis": False,

            "research": {

                "type":
                    research_plan["research_type"],

                "engine":
                    research_plan["engine"],

                "reason":
                    research_plan["reason"]

            },

            "sources":
                results[:5]

        })


    except Exception as e:

        print()
        print("CUROAAGENT ERROR:")
        print(str(e))


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("        CUROAAGENT BACKEND")
    print("==========================================")

    print(
        "Server: http://127.0.0.1:5000"
    )

    print(
        "SerpApi: ENABLED"
    )

    print(
        "Gemini: TEMPORARILY DISABLED"
    )

    print("==========================================")
    print()


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )