from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.config import get_settings  # اضافه کردن این خط برای دسترسی به تنظیمات

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# برای دریافت توکن JWT از هدر درخواست
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# بررسی صحت توکن و استخراج اطلاعات
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # username از توکن استخراج می‌شود
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# بررسی نقش (role) کاربر
def get_role_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")  # نقش (role) از توکن استخراج می‌شود
        if role is None:
            raise credentials_exception
        return role
    except JWTError:
        raise credentials_exception

# تابع is_admin برای چک کردن نقش ادمین
def is_admin(role: str = Depends(get_role_from_token)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have sufficient permissions",
        )
    return True
