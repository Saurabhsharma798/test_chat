from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from database.db import get_db
from services.auth import get_current_user
from models.conversation import Conversation
from schemas.conversation import ConversationOut,ConversationListResponse
router=APIRouter(prefix='/conversation',tags=['conversation'])


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
    return {'conversations':conversations}


@router.get('/{id}',response_model=ConversationOut)
def get_conversation(id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    conversation=db.query(Conversation).filter(Conversation.id==id).first()
    return conversation









