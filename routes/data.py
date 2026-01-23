from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
from db import supabase
from models import ReportCreate

router = APIRouter(prefix="/api")

@router.get("/")
def root():
    return {"message": "API working"}

@router.post("/report")
def create_report(data: ReportCreate, user=Depends(get_current_user)):
    response = supabase.table("reports").insert({
        "user_id": user.id,
        "title": data.title,
        "description": data.description,
        "status": "pending"
    }).execute()

    if response.data is None:
        raise HTTPException(status_code=400, detail="Insert failed")

    return {"message": "Report submitted successfully"}

@router.get("/my-reports")
def get_my_reports(user=Depends(get_current_user)):
    res = supabase.table("reports").select("*").eq("user_id", user.id).execute()
    return res.data
