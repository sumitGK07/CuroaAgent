# =========================================================
# CUROAAGENT - INTELLIGENT RESEARCH ROUTER
# =========================================================

def route_query(query):
    """
    Decide which SerpApi search engine should be used
    for the user's medical question.
    """

    query = query.lower()

    # -----------------------------------------------------
    # MEDICAL RESEARCH / ACADEMIC KEYWORDS
    # -----------------------------------------------------

    research_keywords = [
        "research",
        "study",
        "studies",
        "clinical trial",
        "clinical trials",
        "evidence",
        "paper",
        "papers",
        "journal",
        "meta-analysis",
        "systematic review",
        "scientific",
        "academic",
        "published"
    ]

    # -----------------------------------------------------
    # LATEST / CURRENT MEDICAL INFORMATION
    # -----------------------------------------------------

    news_keywords = [
        "latest",
        "recent",
        "new",
        "newest",
        "current",
        "today",
        "2026",
        "breaking",
        "recent developments",
        "new treatment",
        "latest treatment",
        "new drug",
        "new vaccine",
        "medical breakthrough"
    ]

    # -----------------------------------------------------
    # CHECK FOR RESEARCH INTENT
    # -----------------------------------------------------

    for keyword in research_keywords:

        if keyword in query:

            return {
                "engine": "google_scholar",
                "research_type": "Medical Research",
                "reason": (
                    "Your question asks for scientific "
                    "evidence, studies, or academic research."
                )
            }

    # -----------------------------------------------------
    # CHECK FOR LATEST / NEWS INTENT
    # -----------------------------------------------------

    for keyword in news_keywords:

        if keyword in query:

            return {
                "engine": "google_news",
                "research_type": "Latest Medical News",
                "reason": (
                    "Your question asks for recent or "
                    "current medical information."
                )
            }

    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    return {
        "engine": "google",
        "research_type": "General Medical Search",
        "reason": (
            "This appears to be a general medical "
            "information question."
        )
    }