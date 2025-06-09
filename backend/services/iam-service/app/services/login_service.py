from .user_service import UserService
from .admin_service import AdminService
from .hash_service import HashService
from .auth_tokens import create_access_token  # این همون توکن سازه
from fastapi.security import OAuth2PasswordRequestForm

class LoginService:
    def __init__(self, db):
        self.user_service = UserService(db)
        self.admin_service = AdminService(db)
        self.hash_service = HashService()

    async def login(self, form_data: OAuth2PasswordRequestForm):
        # اول user
        user = await self.user_service.get_by_email_or_mobile(form_data.username)
        if user and self.hash_service.verify_password(form_data.password, user.hashed_password):
            token = create_access_token({"sub": str(user.user_id), "role": "user"})
            return {"access_token": token, "token_type": "bearer"}

        # بعد admin
        admin = await self.admin_service.get_by_email_or_phone(form_data.username)
        if admin and self.hash_service.verify_password(form_data.password, admin.hashed_password):
            token = create_access_token({"sub": str(admin.admin_id), "role": "admin"})
            return {"access_token": token, "token_type": "bearer"}

        return None
