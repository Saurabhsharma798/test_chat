from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session 
from database.db import get_db
from services.auth import get_current_user
from models.conversation import Conversation
from models.message import Message
from models.user import User
from schemas.conversation import ConversationOut,ConversationListResponse
router=APIRouter(prefix='/conversation',tags=['conversation'])


@router.get('/usage')
def get_user_usage(db:Session=Depends(get_db),user=Depends(get_current_user)):
    # count=0
    # conversations=db.query(Conversation).filter(Conversation.user_id==user.id).all()
    # if  not conversations:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="conversation not found")
    

    # for conversation in conversations:
    #     messages=db.query(Message).filter(Message.conversation_id==conversation.id).all()
    #     for message in messages:
    #         if message.role=="user":
    #             count+=1
    # return {'usage':count}
    total_message=db.query(Message).join(Conversation,Message.conversation_id==Conversation.id).filter(Conversation.user_id==user.id).filter(Message.role=="user").count()
    if total_message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='messages not found')
    return total_message


@router.post('/',response_model=ConversationOut)
def create_conversation(db:Session=Depends(get_db),user=Depends(get_current_user)):

    new_conversation=Conversation(
        user_id=user.id
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation


@router.get('/',response_model=ConversationListResponse)
def get_all_conversations(db:Session=Depends(get_db),user=Depends(get_current_user)):
    conversations=db.query(Conversation).filter(Conversation.user_id==user.id).all()
    if not conversations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="conversation not found")
    return {'conversations':conversations}


@router.get('/:{id}',response_model=ConversationOut)
def get_conversation(id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    conversation=db.query(Conversation).filter(Conversation.id==id).first()
    if  conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="conversation not found")
    
    if conversation.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized')
    return conversation




