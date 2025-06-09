from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.domain.models.user import User
from app.domain.models.admin import Admin
from app.services.auth_services.otp_service import OTPService
from app.services.auth_services.hash_service import HashService

router = APIRouter(prefix="/accounts", tags=["accounts"])

# ----- 1. درخواست ارسال OTP (فراموشی رمز عبور) -----
@router.post("/forgot-password")
def forgot_password(email: str, role: str, db: Session = Depends(get_db)):
    if role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'admin'")

    # پیدا کردن کاربر یا ادمین
    if role == "user":
        account = db.query(User).filter(User.email == email).first()
    else:
        account = db.query(Admin).filter(Admin.email == email).first()

    if not account:
        raise HTTPException(status_code=404, detail="No such user or admin found")

    otp = OTPService.generate_otp()
    OTPService.set_otp(email, role, otp)

    # TODO: ارسال ایمیل/پیامک واقعی. فعلاً فقط چاپ برای تست
    print(f"OTP for {email} ({role}) is {otp}")

    return {"msg": "OTP sent to your email/mobile"}

# ----- 2. اعتبارسنجی OTP -----
@router.post("/verify-otp")
def verify_otp(email: str, role: str, otp: str):
    data = OTPService.get_otp(email, role)
    if not data:
        raise HTTPException(status_code=400, detail="OTP expired or not requested")
    if data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"msg": "OTP is valid"}

# ----- 3. ریست رمز عبور -----
@router.post("/reset-password")
def reset_password(
    email: str, 
    role: str, 
    otp: str, 
    new_password: str, 
    db: Session = Depends(get_db)
):
    data = OTPService.get_otp(email, role)
    if not data or data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # پیدا کردن کاربر یا ادمین
    if role == "user":
        account = db.query(User).filter(User.email == email).first()
    else:
        account = db.query(Admin).filter(Admin.email == email).first()

    if not account:
        raise HTTPException(status_code=404, detail="No such user or admin found")

    # هش رمز جدید
    account.hashed_password = HashService().hash_password(new_password)
    db.commit()
    OTPService.delete_otp(email, role)
    return {"msg": "Password reset successful"}
