from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.db.database import get_db
from app.domain.models.user import User
from app.domain.models.admin import Admin

oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
oauth2_admin_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")

def get_current_user_or_admin(
    token: str = Depends(oauth2_user_scheme),  
    db: Session = Depends(get_db),
    is_admin: bool = False  
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_or_admin_id: str = payload.get("sub")
        if not user_or_admin_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if is_admin:
        user_or_admin = db.query(Admin).filter(Admin.id == user_or_admin_id).first() 
    else:
        user_or_admin = db.query(User).filter(User.id == user_or_admin_id).first()  
    if not user_or_admin:
        raise credentials_exception
    return user_or_admin

async def get_current_user(
    token: str = Depends(oauth2_user_scheme),
    db: Session = Depends(get_db)
):
    return await get_current_user_or_admin(token, db, is_admin=False)

async def get_current_admin(
    token: str = Depends(oauth2_admin_scheme),
    db: Session = Depends(get_db)
):
    return await get_current_user_or_admin(token, db, is_admin=True)
