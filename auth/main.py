from datetime import timedelta
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from schemas import UserCreate, UserLogin
from repository import UserRepository
import security

app = FastAPI(title="Auth Microservice")

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if not security.is_password_complex(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not strong enough (minimum 8 characters)"
        )
    
    repo = UserRepository(db)
    new_user = repo.create_user(email=user.email, plain_password=user.password)
    
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return None

@app.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    db_user = repo.get_user_by_email(user.email)
    
    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    access_token = security.create_access_token(
        data={"user_id": db_user.id}, expires_delta=access_token_expires
    )
    
    return {"token": access_token}
