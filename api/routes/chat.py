from fastapi import APIRouter,Depends,HTTPException,status
from models.message import Message
from models.conversation import Conversation
from schemas.message import MessageRequest,MessageResponse,MessageListResponse
from sqlalchemy.orm import Session
from database.db import get_db
from services.auth import get_current_user
from services.llm import call_model

router = APIRouter(prefix='/chat',tags=['chat'])


@router.post('/{chat_id}',response_model=MessageResponse)
def chat(chat_id:int,data:MessageRequest,db:Session=Depends(get_db),user=Depends(get_current_user)):
    conversation=db.query(Conversation).filter(Conversation.id==chat_id).first()
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='conversation not found')
    if conversation.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized')
    conversation_id=chat_id
    content=data.content

    user_message=Message(
        conversation_id=conversation_id,
        role='user',
        content=content
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    response=call_model(conversation_id,db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="ai failed to respond")    

    ai_message=Message(
        conversation_id=conversation_id,
        role="ai",
        content=response.get('content')
    )

    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return response 


@router.get('/{chat_id}',response_model=MessageListResponse)
def get_chat(chat_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    conversation=db.query(Conversation).filter(Conversation.id==chat_id).first()
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='conversation not found')
    if conversation.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized')
    
    chats=db.query(Message).filter(Message.conversation_id==chat_id).all()
    if not chats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="chat not found")
    

    return {'messages':chats}
    
