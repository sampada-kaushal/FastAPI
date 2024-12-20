from fastapi import HTTPException
from dotenv import load_dotenv
import os


load_dotenv()
INITIAL_TOKEN = os.getenv("INITIAL_TOKEN")
class AuthService:

    @staticmethod
    def authenticate(token: str):
        if token!=INITIAL_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorised")