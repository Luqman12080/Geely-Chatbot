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

Only respond with car specifications if the query explicitly mentions a known car model. Do not assume or guess car data. Never mention car specifications unless a specific model is detected in the user query.

If the query is not related to cars (like greetings, thanks, etc.), respond briefly, respectfully, and in a friendly manner. Avoid introducing car-related information in such cases.

Don't mention about any provided data in the response.

Throughly read the data set and use the relevant data to answer the question.

If the result include price, always use 'PKR' with it.

The data contains mutiple vehicles from different brands. Responding to the query according to the data

If a value is 'null' or 'None', don't mention it in the response.

When answering car-related questions, always provide the response using proper **Markdown formatting**:
- Use headings (###) for model names or sections.
- Use bullet points for listing features or specifications.
- Use line breaks for better readability.


Be concise, accurate, and avoid repeating the question in the answer.

Example:
user: "What are the available cars"
Answer: Here are the available car models from all brands:

Geely:
- Geely Monjaro
- Geely Coolray
- Geely EX5
Zeekr
- Zeekr 009
- Zeekr X
- Zeekr 7X
Forthing
- Forthing Friday
JMEV
- JMEV Elight
Riddara
- Riddara RD6
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

# code to load .txt files
file_path = [
    './chatbot_responses.txt'
]

def load_documents(files):
    all_text = []
    for file in files:
        with open(file, 'r', encoding="utf-8-sig") as f:
            content = f.read()
            all_text.append(content) 
    return "\n".join(all_text) 

with open('data.json', 'r') as file:
    car_data = json.load(file)

def extract_model_name(user_input, car_data):
    for model in car_data.keys():
        if model.lower() in user_input.lower():
            return model
    return None


def getMistralResponse(ques, context, data, ques_ans) :
    context += " Do not mention any document or the provided data in the response to the user."
    
    prompt = f"The following car specification data is available:\n{data}\n and in case of any query from user refer the frequently asked question:\n{ques_ans} \n\nThis is user query: {ques}"
    
    # model_name = extract_model_name(ques, data)

    # if model_name:
    #     relevant_data = json.dumps({model_name: data[model_name]}, indent=2)
    #     prompt = f"The following car specification data is available:\n{relevant_data}\n\nThis is the user query: {ques}"
    # else:
    #     prompt = f"This is the user query: {ques}"

    # if session_id not in session_memory:
    #     session_memory[session_id] = []
    
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
    # session_id: str

class ChatResponse(BaseModel):
    response: str 

@app.post("/chat", response_model=ChatResponse )
async def chat_response(request: ChatRequest):
    question = request.input
    print("User Query: ", question)
    # print("Data: ", car_data)
    docs = load_documents(file_path)
    response = getMistralResponse(question,context, car_data, docs)    
    print("Response: ", response)
    return ChatResponse(response=response)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)