import requests

def search_tool(query):
    try:
        # Step 1: Clean query
        cleaned_query = query.lower()

        for word in ["research", "latest", "trend", "analysis"]:
            cleaned_query = cleaned_query.replace(word, "")

        cleaned_query = cleaned_query.strip()

        if not cleaned_query:
            cleaned_query = "artificial intelligence"

        print("CLEANED QUERY:", cleaned_query)

        # Step 2: ALWAYS search first (more reliable)
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={cleaned_query}&format=json"
        search_url=search_url.replace(" ", "%20")
        search_res = requests.get(search_url)
        print("SEARCH URL:", search_url)
        if search_res.status_code != 200:
            return "External data unavailable"

        data = search_res.json()

        results = data.get("query", {}).get("search", [])

        if not results:
            return "External data unavailable"

        # Step 3: Get BEST MATCH title (Wikipedia handles casing)
        best_title = results[0]["title"]
        print("BEST TITLE:", best_title)

        # Step 4: Fetch summary using correct title
        page_query = best_title.replace(" ", "_")
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_query}"

        print("SUMMARY URL:", summary_url)

        summary_res = requests.get(summary_url)

        if summary_res.status_code == 200:
            summary_data = summary_res.json()
            return summary_data.get("extract", "External data unavailable")

        return "External data unavailable"

    except Exception as e:
        return f"External data unavailable"