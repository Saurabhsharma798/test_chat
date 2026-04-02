from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from schemas.auth import Register,Login
from database.db import get_db
from models.user import User
from services.auth import get_user,authenticate_user,hash_password,create_access_token,get_current_user


router=APIRouter(prefix='/auth',tags=['auth'])

@router.post('/register')
def register(data:Register,db:Session=Depends(get_db)):
    # user=db.query(User).filter(User.email==data.email).first()

    user=get_user(db=db,email=data.email)

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    password=hash_password(data.password)
    new_user=User(email=data.email,hashed_password=password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'message':'user created successfully'}
    


@router.post('/login')
def login(data:Login,db:Session=Depends(get_db)):
    
    user=authenticate_user(db,data.email,data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token=create_access_token(data={'sub':user.email})

    return {'token':access_token,'token_type':"Bearer"}

    
@router.get('/protected')
def protected(user=Depends(get_current_user)):
    return {'message':f'{user.email} is current user'}

