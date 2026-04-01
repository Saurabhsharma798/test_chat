from pydantic import BaseModel


class MessageRequest(BaseModel):
    content:str


class MessageResponse(BaseModel):
    role:str
    content:str

    model_config={'from_attributes':True}

class MessageListResponse(BaseModel):
    messages:list[MessageResponse]