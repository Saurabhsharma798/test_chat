from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from database.db import Base
from models.conversation import Conversation
from datetime import datetime,timezone


class Message(Base):
    __tablename__ = "message"

    id=Column(Integer,primary_key=True,index=True)
    conversation_id = Column(Integer,ForeignKey(Conversation.id),nullable=False)
    role=Column(String,nullable=False)
    content = Column(String,nullable=False)

    created_at=Column(DateTime,default=datetime.now(timezone.utc))

    model_config={'from_attributes':True}


    
