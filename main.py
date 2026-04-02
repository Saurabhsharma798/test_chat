from fastapi import FastAPI,APIRouter
from api.routes.auth import router as auth_route
from api.routes.chat import router as chat_route
from api.routes.conversation import router as conversation_route
from database.db import create_table

app=FastAPI()
app.include_router(auth_route)
app.include_router(chat_route)
app.include_router(conversation_route)


create_table()

@app.get('/health')
def health():
    return {"status":"ok"}

