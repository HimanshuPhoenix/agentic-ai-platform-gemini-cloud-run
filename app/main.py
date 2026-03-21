from fastapi import FastAPI
from app.agent.agent import run_agent

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Agent running 🚀"}

@app.post("/query")
def query(user_input: str):
    return {"response": run_agent(user_input)}