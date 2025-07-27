from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents import Assistant
from database import log_interaction, setup_database
import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

try:
    assistant = Assistant()
    setup_database()
    print("✅ System initialized successfully!")
except Exception as e:
    print(f"❌ Initialization failed: {str(e)}")
    exit(1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        response, agent = assistant.handle_query(request.query)
        log_interaction(request.query, agent, response)
        return {"response": response, "agent": agent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)