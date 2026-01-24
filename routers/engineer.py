from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Engineer
from auth import hash_password, verify_password
from schemas.engineer_schema import (
    EngineerRegister,
    EngineerLogin,
    EngineerResetPassword
)

router = APIRouter(prefix="/api", tags=["Engineer"])


@router.post("/register")
def register_engineer(data: EngineerRegister, db: Session = Depends(get_db)):
    if db.query(Engineer).filter(Engineer.userId == data.userId).first():
        raise HTTPException(status_code=400, detail="Engineer already exists")

    engineer = Engineer(
        userId=data.userId,
        password=hash_password(data.password),
        ward=data.ward
    )

    db.add(engineer)
    db.commit()
    return {"message": "Engineer registered successfully"}


@router.post("/login")
def login_engineer(data: EngineerLogin, db: Session = Depends(get_db)):
    engineer = db.query(Engineer).filter(
        Engineer.userId == data.userId
    ).first()

    if not engineer or not verify_password(data.password, engineer.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "userId": engineer.userId,
        "ward": engineer.ward
    }


@router.post("/forgot-password")
def forgot_password(
    data: EngineerResetPassword,
    db: Session = Depends(get_db)
):
    engineer = db.query(Engineer).filter(
        Engineer.userId == data.userId
    ).first()

    if not engineer:
        raise HTTPException(status_code=404, detail="Engineer not found")

    engineer.password = hash_password(data.newPassword)
    db.commit()

    return {"message": "Password updated successfully"}