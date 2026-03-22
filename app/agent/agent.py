import os
from google import genai
from dotenv import load_dotenv
from app.tools.search_tool import search_tool

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def run_agent(user_input: str):

    tool_data = ""
    hallucination_check = "✅ This response is grounded in retrieved external data to reduce hallucination."

    if any(word in user_input.lower() for word in ["research", "latest", "trend", "analysis"]):
        tool_data = search_tool(user_input)

    if not tool_data or len(tool_data.strip()) < 50:
        tool_data = "External data unavailable"
        hallucination_check = "⚠️ External data retrieval failed, so the response may rely more on general knowledge. Be cautious of potential hallucinations."

    plan = f"User wants information about: {user_input}"
    tool_data = tool_data[:1000]  # limit size
    print("TOOL DATA USED:", tool_data[:200])
    prompt = f"""
        You are an advanced AI agent.

        Your job is to:
        1. Understand the user query
        2. Analyze available data
        3. Provide structured insights

        STRICT INSTRUCTIONS:
        - You MUST use the External Data provided below
        - Do NOT rely only on your own knowledge
        - If External Data is meaningful, use it clearly in your answer
        - If External Data is weak or missing, supplement with your own knowledge

        User Query:
        {user_input}

        External Data:
        {tool_data}

        Agent Plan:
        {plan}

        
        Respond in the following format:

        🧠 Understanding:
        (What the user is asking)

        📊 Key Insights:
        (Bullet points)

        ⚠️ Observations / Risks:
        (If applicable)

        🎯 Confidence Score:
        (Give a confidence level from 1-10)

        Sources:
        (Mention if information is derived from external data)

        🔧 Tools Used:
        - External API (Wikipedia)

        ✅ Final Answer:
        (Clear and concise response)

        📌 Note:
        {hallucination_check}

        TOOL DATA response: {tool_data}
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Error occurred: {str(e)}"