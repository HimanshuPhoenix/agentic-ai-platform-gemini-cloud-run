import requests

def search_tool(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    
    res = requests.get(url)
    
    if res.status_code == 200:
        return res.json().get("extract", "No data found")
    
    return "Error fetching data"