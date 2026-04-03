# MindAPI

An AI Assistent ChatApp where you can signup and chat with your own personalized ai assistent

## Tech Stack

- FastAPI
- PostgreSQL
- SQLite
- LangChain
- Gemini
- JWT

## Features
- User registration and JWT authentication
- Create and manage multiple conversations
- Chat with Gemini AI with persistent conversation memory
- Usage tracking per user


## API Endpoints

# Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register | Register new user | No |
| POST | /auth/login | Login and get token | No |

# Chat

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /chat/{id} | send a new message | Yes |
| GET | /chat/{id} | get all your message with a conversation id | Yes |

# Conversation

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /conversation | Create new conversation | Yes |
| GET | /conversation | Get all your conversation | Yes |
| GET | /conversation/{id} | Get a particular  conversation | Yes |
| GET | /conversation/usage | Get total user usage | Yes |

# Health

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /health | Check Server Running Status | No |
| GET | /protected | Check Current user | Yes |

## How to Run Locally

1. Clone the repo
```
git clone 
```
2. Create virtual environment
```
cd mindapi
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create .env file (see Environment Variables)
```
touch .env
```
5. Run the server
```
uvicorn main:app --reload
```

## Environment Variables

Create a `.env` file with these variables:
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
DATABASE_URL=
GOOGLE_API_KEY=


## Live API
coming soon