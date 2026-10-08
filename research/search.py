# =========================================================
# CUROAAGENT - SERPAPI RESEARCH ENGINE
# =========================================================

import os
import requests
from dotenv import load_dotenv


# Load .env
load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_medical(query, engine):
    """
    Search SerpApi using the selected research engine.

    Supported engines:
    - google
    - google_scholar
    - google_news
    """

    if not SERPAPI_KEY:
        return {
            "success": False,
            "error": "SERPAPI_KEY not found in .env file.",
            "results": []
        }


    # -----------------------------------------------------
    # SERPAPI PARAMETERS
    # -----------------------------------------------------

    params = {
        "engine": engine,
        "q": query,
        "api_key": SERPAPI_KEY
    }


    # Keep the number of results small
    # because the free SerpApi plan is limited.
    if engine == "google":
        params["num"] = 5

    elif engine == "google_scholar":
        params["num"] = 5

    elif engine == "google_news":
        params["num"] = 5


    # -----------------------------------------------------
    # SEND REQUEST
    # -----------------------------------------------------

    try:

        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()


    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "SerpApi request timed out.",
            "results": []
        }


    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"SerpApi connection error: {e}",
            "results": []
        }


    except ValueError:

        return {
            "success": False,
            "error": "SerpApi returned an invalid response.",
            "results": []
        }


    # -----------------------------------------------------
    # SERPAPI ERROR
    # -----------------------------------------------------

    if "error" in data:

        return {
            "success": False,
            "error": data["error"],
            "results": []
        }


    # -----------------------------------------------------
    # GET RESULTS
    # -----------------------------------------------------

    if engine == "google_news":

        raw_results = data.get(
            "news_results",
            []
        )

    else:

        raw_results = data.get(
            "organic_results",
            []
        )


    # -----------------------------------------------------
    # NORMALIZE RESULTS
    # -----------------------------------------------------

    results = []


    for result in raw_results[:5]:

        title = result.get(
            "title",
            "Unknown source"
        )

        snippet = result.get(
            "snippet",
            ""
        )

        link = result.get(
            "link",
            ""
        )


        # Different SerpApi engines may provide
        # different source fields.
        source = result.get(
            "source",
            ""
        )


        # Google News may use source as a dictionary
        if isinstance(source, dict):

            source = source.get(
                "name",
                ""
            )


        results.append(
            {
                "title": title,
                "snippet": snippet,
                "link": link,
                "source": source
            }
        )


    # -----------------------------------------------------
    # NO RESULTS
    # -----------------------------------------------------

    if not results:

        return {
            "success": False,
            "error": "No useful research results were found.",
            "results": []
        }


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return {
        "success": True,
        "error": None,
        "results": results
    }