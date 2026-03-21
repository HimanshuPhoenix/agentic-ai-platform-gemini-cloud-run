import os
from google import genai
from dotenv import load_dotenv
from app.tools.search_tool import search_tool

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def run_agent(user_input: str):

    tool_data = ""

    if "research" in user_input.lower():
        tool_data = search_tool(user_input)

    prompt = f"""
You are an intelligent AI agent.

User Query:
{user_input}

External Data:
{tool_data}

Instructions:
- Understand the query
- Use external data if available
- Provide a structured, helpful response
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error occurred: {str(e)}"