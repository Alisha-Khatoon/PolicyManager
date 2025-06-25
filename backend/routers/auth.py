from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
import httpx
import uuid

from backend.db.session import get_db
from backend.models.auth import User
from backend.core.security import create_access_token
from backend.core.config import settings

router = APIRouter()

@router.get("/google/login")
async def google_login():
    from urllib.parse import urlencode
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    return {"url": f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"}

@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    try:
        # Token exchange with Google
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            # IMPORTANT: Raise an exception for bad responses (4xx or 5xx)
            response.raise_for_status() # <--- This line is crucial
            tokens = response.json()

        # Verify ID token
        id_info = id_token.verify_oauth2_token(
            tokens["id_token"],
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        # Create or get user
        user = db.query(User).filter(User.email == id_info["email"]).first()
        if not user:
            user = User(
                id=str(uuid.uuid4()),
                email=id_info["email"],
                name=id_info.get("name"),
                google_id=id_info["sub"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return {
            "access_token": create_access_token({"sub": user.id}),
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except httpx.HTTPStatusError as e:
        # Catch specific HTTP errors from the token exchange
        print(f"HTTP error during token exchange: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Google token exchange failed: {e.response.text}"
        )
    except Exception as e:
        # Catch other potential errors during the callback process
        print(f"Error during Google callback: {e}")
        raise HTTPException(status_code=400, detail=f"Google authentication failed: {str(e)}")