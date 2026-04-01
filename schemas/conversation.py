from pydantic import BaseModel
from datetime import datetime



class ConversationOut(BaseModel):
    id:int
    user_id:int
    created_at:datetime

    model_config={'from_attributes':True}

class ConversationListResponse(BaseModel):
    conversations:list[ConversationOut]