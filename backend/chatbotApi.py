from fastapi import FastAPI, Request, HTTPException
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from fastapi import Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import requests
from typing import Optional
import logging
import hmac
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

context = """
You are a helpful and intelligent AI assistant and the official virtual assistant for **Capital Smart Motors (CSM Motors)**. You specialize in answering questions about car models and specifications offered exclusively by CSM Motors.

You are also capable of responding politely to general conversation, greetings, thanks, and casual small talk.

Only respond with car specifications if the query explicitly mentions a known car model. Do not assume or guess car data. Never mention car specifications unless a specific model is detected in the user query.

If the query is not related to cars (like greetings, thanks, etc.), respond briefly, respectfully, and in a friendly manner. Avoid introducing car-related information in such cases.

CRITICAL: Never mention "dataset", "provided data", "my data", "the information I have", "not specified" or any reference to data sources in your responses. Always speak naturally as a knowledgeable CSM Motors assistant.

When a customer asks about a car brand or model that is NOT offered by CSM Motors, respond like this:
- "We currently don't deal in [car name]. However, at Capital Smart Motors, we proudly offer the following brands and models: [list the available brands/models]. Feel free to ask about any of these!"
- Or: "That vehicle isn't part of our current lineup at Capital Smart Motors. We currently offer [list brands]. Would you like to know more about any of these?"
- Never say "This is not in my dataset" or "I don't have that in my data."

When information about a CSM Motors car is not available:
- Say: "I don't have specific details about that at the moment. Please contact our sales team for further assistance."
- Or: "For more details on that, I recommend reaching out to our customer service team directly."

Thoroughly read the available information and use the relevant details to answer the question.

If the result includes price, always use 'PKR' with it.

The information contains multiple vehicles from different brands all offered exclusively by Capital Smart Motors. Respond to the query according to the available details.

If a value is 'null' or 'None', don't mention it in the response.

When answering car-related questions, always provide the response using proper **Markdown formatting**:
- Use headings (###) for model names or sections.
- Use bullet points for listing features or specifications.
- Use line breaks for better readability.

Be concise, accurate, and avoid repeating the question in the answer.

Example:
user: "What are the available cars"
Answer: Here are the car models currently offered by Capital Smart Motors:

Zeekr:
- Zeekr 009
- Zeekr X
- Zeekr 7X
Forthing:
- Forthing Friday
JMEV:
- JMEV Elight
Riddara:
- Riddara RD6
"""

# Global in-memory store for session memory
session_memory = {}  # { session_id: [ChatMessage, ...] }
MAX_HISTORY = 10     # Keep last 10 exchanges


# Initialize Mistral AI client
MISTRAL_API_KEY = "3fpWuiSPSYfbRTZamjen0z0tSZb0KL2E"
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # You create this
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET") 

WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

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

def format_for_whatsapp(text):
    """
    Convert markdown to WhatsApp formatting
    """
    # Convert **bold** to *bold* for WhatsApp
    text = text.replace('**', '*')
    # Remove ### headers (WhatsApp doesn't support them well)
    text = text.replace('###', '')
    return text.strip()

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
    

def send_whatsapp_message(to_phone_number, message_text):
    """
    Send a message via WhatsApp Business API
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Format message for WhatsApp
    formatted_message = format_for_whatsapp(message_text)
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": formatted_message
        }
    }
    
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully to {to_phone_number}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send WhatsApp message: {str(e)}")
        if hasattr(e.response, 'text'):
            logger.error(f"Response: {e.response.text}")
        raise

def mark_message_as_read(message_id):
    """
    Mark a message as read
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }
    
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to mark message as read: {str(e)}")

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

@app.post("/twilio-webhook")
async def twilio_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    """
    Twilio WhatsApp webhook endpoint
    """

    logger.info(f"Twilio message from {From}: {Body}")

    try:
        docs = load_documents(file_path)

        bot_response = getMistralResponse(
            Body,
            context,
            car_data,
            docs
        )

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        bot_response = "Sorry, something went wrong."

    resp = MessagingResponse()
    resp.message(format_for_whatsapp(bot_response))

    return Response(content=str(resp), media_type="application/xml")

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification endpoint for Meta
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verified successfully!")
        return int(challenge)
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Main webhook endpoint to receive WhatsApp messages
    """
    try:
        body = await request.json()
        logger.info(f"Webhook received: {json.dumps(body, indent=2)}")
        
        # Verify webhook signature (optional but recommended for production)
        # if WEBHOOK_SECRET:
        #     signature = request.headers.get("X-Hub-Signature-256", "")
        #     if not verify_webhook_signature(await request.body(), signature):
        #         raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Extract message data
        if body.get("object") == "whatsapp_business_account":
            entries = body.get("entry", [])
            
            for entry in entries:
                changes = entry.get("changes", [])
                
                for change in changes:
                    value = change.get("value", {})
                    
                    # Check if it's a message
                    if "messages" in value:
                        messages = value.get("messages", [])
                        
                        for message in messages:
                            message_id = message.get("id")
                            from_number = message.get("from")
                            message_type = message.get("type")
                            
                            # Handle text messages
                            if message_type == "text":
                                user_message = message.get("text", {}).get("body", "")
                                logger.info(f"Received message from {from_number}: {user_message}")
                                
                                # Mark message as read
                                mark_message_as_read(message_id)
                                
                                # Generate response using your chatbot
                                bot_response = getMistralResponse(
                                    user_message, 
                                    context, 
                                    car_data, 
                                    docs,
                                    # session_id=from_number  # Use phone number as session ID
                                )
                                
                                # Send response back via WhatsApp
                                send_whatsapp_message(from_number, bot_response)
                            
                            # Handle other message types (optional)
                            elif message_type == "image":
                                send_whatsapp_message(
                                    from_number, 
                                    "I received your image! However, I currently only process text messages. Please describe what you'd like to know about our cars."
                                )
                            elif message_type in ["audio", "video", "document"]:
                                send_whatsapp_message(
                                    from_number, 
                                    "I can only process text messages at the moment. Please send your question as text."
                                )
        
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify webhook signature for security (production use)
    """
    if not WEBHOOK_SECRET:
        return True
    
    expected_signature = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Car Chatbot API",
        "endpoints": {
            "web_chat": "/chat",
            "whatsapp_webhook": "/webhook"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)