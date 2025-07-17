from fastapi import FastAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

context = """
You are a helpful and intelligent AI assistant specialized in answering questions about car models and specifications from a known data set. 
You are also capable of responding politely to general conversation, greetings, thanks, and casual small talk.

If the user asks a question that contains the name of a known car model, try to extract the correct specification and answer accurately from that data.

If the query is not related to cars (like greetings, thanks, etc.), still respond helpfully and politely. Keep answers short and respectful.
"""

# Global in-memory store for session memory
session_memory = {}  # { session_id: [ChatMessage, ...] }
MAX_HISTORY = 10     # Keep last 10 exchanges


# Initialize Mistral AI client
MISTRAL_API_KEY = "3fpWuiSPSYfbRTZamjen0z0tSZb0KL2E"  # Replace with your actual API key
client = MistralClient(api_key=MISTRAL_API_KEY)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('data.json', 'r') as file:
    car_data = json.load(file)

def getMistralResponse(ques, context, data, session_id) :
    context += " Do not mention any document in the response. and also mention in the response that ai based data can be incorrect."

        
    prompt = f"The following car specification data is available:\n{data}\n\nQuestion of user: {ques}\nAnswer:"

    if session_id not in session_memory:
        session_memory[session_id] = []
    
    try:
        messages = [
            ChatMessage(role="system", content=context),
            ChatMessage(role="user", content=prompt)
        ]
        response = client.chat(model="mistral-tiny", messages=messages)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error fetching AI response: {str(e)}"
    

class ChatRequest(BaseModel):
    input: str
    session_id: str

class ChatResponse(BaseModel):
    response: str 

@app.post("/chat", response_model=ChatResponse )
async def chat_response(request: ChatRequest):
    question = request.input
    session = request.session_id
    # print("Data: ", car_data)
    response = getMistralResponse(question,context, car_data,session)    
    return ChatResponse(response=response)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)