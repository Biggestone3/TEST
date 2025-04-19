import os
import urllib.parse
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from jose import jwt
from lna_db.models.news import User
from pydantic import BaseModel

router = APIRouter()


# Security configuration
class CodePayload(BaseModel):
    """
    Pydantic model to accept the code sent by Google in the POST request body.
    We were originally sending the code as a query parameter, but Google doesn't
    always accept that format. Switching to a JSON body aligns better with the
    auth-code flow and helps avoid the bad request error.
    """

    code: str


@router.get("/google")
async def auth_google() -> RedirectResponse:
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={os.getenv('GOOGLE_CLIENT_ID')}&"
        f"redirect_uri={os.getenv('GOOGLE_REDIRECT_URI')}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )


# auth.py
@router.post("/google/callback")
async def google_callback(payload: CodePayload) -> dict[str, str]:
    code = payload.code
    """Improved with detailed error logging"""
    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
            redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
            if not client_id:
                raise RuntimeError("GOOGLE_CLIENT_ID is not set in the environment!")
            if not client_secret:
                raise RuntimeError(
                    "GOOGLE_CLIENT_SECRET is not set in the environment!"
                )
            if not redirect_uri:
                raise RuntimeError("GOOGLE_REDIRECT_URI is not set in the environment!")
            encoded_payload = urllib.parse.urlencode(
                {
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": "postmessage",
                    "grant_type": "authorization_code",
                }
            )

            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                content=encoded_payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            token_response.raise_for_status()
            tokens = token_response.json()

        # Verify ID token
        idinfo = id_token.verify_oauth2_token(
            tokens["id_token"], google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )

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
        raise HTTPException(status_code=400, detail=e.response.text)

    except ValueError as e:
        print(" Token Validation Error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as e:
        print(" Unexpected Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/logout")
async def logout() -> JSONResponse:
    """Logout user by invalidating the JWT (handled on the client side)"""
    # You could return a message confirming the logout, but JWT tokens are stateless,
    # so the actual "logout" happens when the token is removed from the client.
    return JSONResponse(content={"message": "Successfully logged out"}, status_code=200)
