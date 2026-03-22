from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
load_dotenv()

import os

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN")

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )

    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )

    return credentials.credentials