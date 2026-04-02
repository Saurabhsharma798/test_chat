from pwdlib import PasswordHash
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from datetime import timedelta,datetime,timezone
import jwt
from models.user import User
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from database.db import get_db
from core.config import settings


SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES






password_hash=PasswordHash.recommended()
# oauth2_scheme=OAuth2PasswordBearer(tokenUrl='auth/login')
security=HTTPBearer()


def hash_password(password):
    return password_hash.hash(password)


def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)


#to fetch user from db
def get_user(db,email):
    user=db.query(User).filter(User.email==email).first()
    return user
    

#to authenticate user
def authenticate_user(db,email:str,password:str):
    user=get_user(db=db,email=email)
    if not user or not verify_password(password,user.hashed_password):
        return False
    return user


#to create access token
def create_access_token(data:dict,expire_delta:timedelta | None= None):
    to_encode=data.copy()
    if expire_delta:
        expire=datetime.now(timezone.utc)+expire_delta

    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt


def get_current_user(token:HTTPAuthorizationCredentials=Depends(security),db:Session=Depends(get_db)):
    try:
        token=token.credentials
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_email = payload.get("sub")

        if user_email is None:
            return {'user email  not found'}
        
        user=get_user(db,user_email)
        if user is None:
            return {'user not in db'}
        
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

