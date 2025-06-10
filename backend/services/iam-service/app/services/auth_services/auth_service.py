from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, hash_service, user_service, admin_service):
        self.hash_service = hash_service
        self.user_service = user_service
        self.admin_service = admin_service

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_via_oauth(self, form_data):

        user = self.user_service.get_by_email_or_mobile(form_data.username, form_data.username)
        if user and self.hash_service.verify_password(form_data.password, user.hashed_password):
            access_token = self.create_access_token({"sub": str(user.id), "role": "user"})
            return {"access_token": access_token, "token_type": "bearer"}


        admin = self.admin_service.get_by_email_or_phone(form_data.username, form_data.username)
        if admin and self.hash_service.verify_password(form_data.password, admin.hashed_password):
            access_token = self.create_access_token({"sub": str(admin.id), "role": "admin"})
            return {"access_token": access_token, "token_type": "bearer"}

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
