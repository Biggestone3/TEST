import os
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from jose import jwt
from lna_db.models.news import User

router = APIRouter()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/google")
async def auth_google():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={os.getenv('GOOGLE_CLIENT_ID')}&"
        f"redirect_uri={os.getenv('GOOGLE_REDIRECT_URI')}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )


# auth.py
@router.post("/google/callback")
async def google_callback(code: str = Query(...)):
    """Improved with detailed error logging"""
    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
                    "grant_type": "authorization_code",
                },
            )

            # Log raw Google response
            print("Google Token Response:", token_response.text)

            token_response.raise_for_status()
            tokens = token_response.json()

        # Verify ID token
        idinfo = id_token.verify_oauth2_token(
            tokens["id_token"], google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )
        print("Verified User Info:", idinfo)

        # Find/create user
        user = await User.find_one({"google_id": idinfo["sub"]})
        if not user:
            user = User(
                google_id=idinfo["sub"],
                email=idinfo["email"],
                full_name=idinfo.get("name", ""),
                username=idinfo.get("email", "").split("@")[0],
            )
            await user.save()  # type: ignore[attr-defined]
            print("Created new user:", user.id)

        # Generate JWT
        secret = os.getenv("SECRET_KEY")
        if not secret:
            raise ValueError("Missing SECRET_KEY in environment")

        access_token = jwt.encode(
            {"sub": user.google_id, "exp": datetime.utcnow() + timedelta(hours=1)},
            secret,
            algorithm="HS256",
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except httpx.HTTPStatusError as e:
        print(" HTTP Error:", e.response.text)
        raise HTTPException(status_code=400, detail="Google API error")

    except ValueError as e:
        print(" Token Validation Error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as e:
        print(" Unexpected Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/logout")
async def logout():
    """Logout user by invalidating the JWT (handled on the client side)"""
    # You could return a message confirming the logout, but JWT tokens are stateless,
    # so the actual "logout" happens when the token is removed from the client.
    return JSONResponse(content={"message": "Successfully logged out"}, status_code=200)
