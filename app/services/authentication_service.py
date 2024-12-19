from fastapi import HTTPException

class AuthService:
    
    INITIAL_TOKEN="QWERTY123"

    @staticmethod
    def authenticate(token: str):
        if token!=AuthService.INITIAL_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorised")