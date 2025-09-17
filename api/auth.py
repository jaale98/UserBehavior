from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt 
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from api.db import get_db
from api.models import User
from api.schemas import RegisterIn, LoginIn, TokenOut, UserOut
from api.settings import settings

router = APIRouter()

def create_access_token(*, user_id: int, username: str, expires_minutes: int | None = None) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expires_minutes
    )
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
        "iat": datetime.now(tz=timezone.utc),
    }
    token = jwt.encode(payload, settings.app_secret_key, algorithm=settings.jwt_algorithm)
    return token

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.app_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_authorization_token(authorization: Optional[str] = Header(default=None)) -> str:
    """
    Extracts a Bearer token from the Authorization header.
    Accepts: "Authorization: Bearer <token>"
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")
    return parts[1]

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_authorization_token)) -> User:
    data = decode_access_token(token)
    user_id = int(data.get("sub", "0"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    """
    Minimal registration: creates a new user with a hashed password.
    In a real app: rate-limit, stronger password rules, email verification
    """
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    
    user = User(
        username=payload.username,
        password_hash=generate_password_hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not check_password_hash(user.password_hash, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(user_id=user.id, username=user.username)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user