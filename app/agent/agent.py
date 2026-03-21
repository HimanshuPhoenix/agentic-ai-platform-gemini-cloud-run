from app.tools.search_tool import search_tool

def run_agent(user_input: str):
    if "research" in user_input.lower():
        data = search_tool(user_input)
        return f"🔍 Research Result:\n{data}"
    
    return f"🤖 Echo: {user_input}"