from sqlalchemy import Column,Integer,ForeignKey,DateTime
from database.db import Base
from models.user import User
from datetime import datetime,timezone


class Conversation(Base):
    __tablename__ = "conversation"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey(User.id),nullable=False)
    created_at=Column(DateTime,default=datetime.now(timezone.utc))

    model_config={'from_attributes':True}


