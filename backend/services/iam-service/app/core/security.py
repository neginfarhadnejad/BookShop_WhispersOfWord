from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.db.database import get_db
from app.domain.models.user import User
from app.domain.models.admin import Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user_or_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_or_admin_id: str = payload.get("sub")
        role: str = payload.get("role")
        if not user_or_admin_id or not role:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if role == "admin":
        user_or_admin = db.query(Admin).filter(Admin.id == user_or_admin_id).first() 
    else:
        user_or_admin = db.query(User).filter(User.id == user_or_admin_id).first()  

    if not user_or_admin:
        raise credentials_exception

    user_or_admin.role = role
    return user_or_admin

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user_or_admin(token, db)
    if getattr(user, "role", None) != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User access only.")
    return user

def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    admin = get_current_user_or_admin(token, db)
    if getattr(admin, "role", None) != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access only.")
    return admin
