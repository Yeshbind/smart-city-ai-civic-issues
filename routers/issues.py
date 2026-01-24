from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends, Query, Request
from services.ai_client import call_ai
from schemas.issue import Issue
from db import get_db
from models import Issue as IssueModel
from sqlalchemy.orm import Session
import os
import uuid

router = APIRouter()

# Confidence threshold (can be tuned via .env)
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))

# Valid issue types detected by AI (hackathon scope)
VALID_ISSUES = {"pothole", "garbage"}


@router.post("/detect-violation", response_model=Issue)
def detect_violation(
    file: UploadFile = File(...),
    lat: float | None = Form(None),
    lng: float | None = Form(None),
    timestamp: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """
    Accept image from survey app, forward to AI service,
    apply confidence rules, store and return issue.
    """

    # Save the uploaded image
    filename = f"{uuid.uuid4()}.jpg"
    os.makedirs("uploads", exist_ok=True)
    with open(f"uploads/{filename}", "wb") as f:
        f.write(file.file.read())

    # 1️⃣ Call AI service
    try:
        ai_resp = call_ai(file)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI service unavailable: {e}"
        )

    detections = ai_resp.get("detections", [])

    # 2️⃣ No detections from AI
    if not detections:
        issue = IssueModel(
            title="No Issue Detected",
            description="AI detected no issues in the image",
            ward="unknown",
            status="no_issue_detected",
            before_image=filename,
            category="none",
            confidence=0.0,
            severity=0.0,
            priority="low",
            latitude=str(lat) if lat else None,
            longitude=str(lng) if lng else None,
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return {
            "id": issue.id,
            "issue_type": issue.category,
            "confidence": issue.confidence,
            "status": issue.status,
            "bbox": None,
            "source": "ai_detection",
            "lat": float(issue.latitude) if issue.latitude else None,
            "lng": float(issue.longitude) if issue.longitude else None,
            "timestamp": issue.created_at.isoformat() if issue.created_at else None,
            "priority": issue.priority,
            "assignedTo": None,
            "notes": None,
        }

    # 3️⃣ Take first detection
    det = detections[0]
    cls = det.get("class") or det.get("label") or det.get("issue_type")

    try:
        confidence = float(det.get("confidence", 0))
    except Exception:
        confidence = 0.0

    bbox = det.get("bbox")

    # 4️⃣ Ignore unsupported classes
    if cls not in VALID_ISSUES:
        issue = IssueModel(
            title="Unsupported Issue",
            description=f"Detected {cls} but not supported",
            ward="unknown",
            status="no_issue_detected",
            before_image=filename,
            category="none",
            confidence=confidence,
            severity=confidence,
            priority="low",
            latitude=str(lat) if lat else None,
            longitude=str(lng) if lng else None,
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return {
            "id": issue.id,
            "issue_type": issue.category,
            "confidence": issue.confidence,
            "status": issue.status,
            "bbox": bbox,
            "source": "ai_detection",
            "lat": float(issue.latitude) if issue.latitude else None,
            "lng": float(issue.longitude) if issue.longitude else None,
            "timestamp": issue.created_at.isoformat() if issue.created_at else None,
            "priority": issue.priority,
            "assignedTo": None,
            "notes": None,
        }

    # 5️⃣ Apply confidence rule
    status_str = "open"  # Always set to "open" as per task

    severity = confidence * 10  # Scale to 0-10
    priority = "high" if severity >= 7 else "medium" if severity >= 4 else "low"

    issue = IssueModel(
        title=f"Detected {cls}",
        description=f"AI detected {cls} with confidence {confidence}",
        ward="unknown",
        status=status_str,
        before_image=filename,
        category=cls,
        confidence=confidence,
        severity=severity,
        priority=priority,
        latitude=str(lat) if lat else None,
        longitude=str(lng) if lng else None,
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    print("AI DETECTION:", cls, confidence)

    return {
        "id": issue.id,
        "issue_type": issue.category,
        "confidence": issue.confidence,
        "status": issue.status,
        "bbox": bbox,
        "source": "ai_detection",
        "lat": float(issue.latitude) if issue.latitude else None,
        "lng": float(issue.longitude) if issue.longitude else None,
        "timestamp": issue.created_at.isoformat() if issue.created_at else None,
        "priority": issue.priority,
        "assignedTo": None,
        "notes": None,
    }


@router.get("/issues", response_model=list[Issue])
def get_issues(ward: str | None = Query(None), request: Request = None, db: Session = Depends(get_db)):
    if ward:
        issues = db.query(IssueModel).filter(IssueModel.ward == ward).order_by(IssueModel.created_at.desc()).all()
    else:
        issues = db.query(IssueModel).order_by(IssueModel.created_at.desc()).all()
    base_url = str(request.base_url).rstrip("/")
    return [
        {
            "id": issue.id,
            "issue_type": issue.category or "unknown",
            "confidence": issue.confidence or 0.0,
            "status": issue.status,
            "bbox": None,
            "source": "ai_detection",
            "lat": float(issue.latitude) if issue.latitude else None,
            "lng": float(issue.longitude) if issue.longitude else None,
            "timestamp": issue.created_at.isoformat() if issue.created_at else None,
            "priority": issue.priority,
            "assignedTo": None,
            "notes": None,
            "severity": issue.severity,
            "before_image": f"{base_url}/uploads/{issue.before_image}" if issue.before_image else None,
            "after_image": f"{base_url}/uploads/{issue.after_image}" if issue.after_image else None,
        }
        for issue in issues
    ]


@router.put("/issues/{issue_id}", response_model=Issue)
def put_issue(issue_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Not found")

    allowed = {"status", "priority", "assignedTo", "notes"}
    for k, v in payload.items():
        if k in allowed:
            setattr(issue, k, v)

    db.commit()
    db.refresh(issue)

    return {
        "id": issue.id,
        "issue_type": issue.category or "unknown",
        "confidence": issue.confidence or 0.0,
        "status": issue.status,
        "bbox": None,
        "source": "ai_detection",
        "lat": float(issue.latitude) if issue.latitude else None,
        "lng": float(issue.longitude) if issue.longitude else None,
        "timestamp": issue.created_at.isoformat() if issue.created_at else None,
        "priority": issue.priority,
        "assignedTo": None,
        "notes": None,
    }


@router.post("/issues/{issue_id}/after-image")
def upload_after_image(issue_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    filename = f"{uuid.uuid4()}.jpg"
    os.makedirs("uploads", exist_ok=True)
    with open(f"uploads/{filename}", "wb") as f:
        f.write(file.file.read())

    issue.after_image = filename
    issue.status = "resolved"
    db.commit()

    return {"message": "After image uploaded and issue resolved"}
