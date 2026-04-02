from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import get_db
from models.message import Message
import json
from langchain_core.messages import HumanMessage,AIMessage
from core.config import settings



model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=50,
    timeout=None,
    max_retries=2,
    # other params...
)



def get_conversation_history(conversation_id,db:Session):
    messages=db.query(Message).filter(Message.conversation_id==conversation_id).all()
    formatted_messages=[]
    for message in messages:
        if message.role=='user':
            formatted_messages.append(HumanMessage(content=message.content))
        if message.role=="ai":
            formatted_messages.append(AIMessage(content=message.content))
    return formatted_messages

def call_model(conversation_id,db:Session):
    messages=get_conversation_history(db=db,conversation_id=conversation_id)
    print('----------------------------')
    print("calling model")
    response=model.invoke(messages)
    print('----------------------------')
    print(response)
    print('----------------------------')

    return {'role':'ai','content':response.content}

