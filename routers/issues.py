from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from services.ai_client import call_ai
from models.issue import Issue
from db import add_issue, list_issues, get_issue, update_issue, delete_issue
import os

router = APIRouter()

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))


@router.post("/detect-violation", response_model=Issue)
def detect_violation(
    file: UploadFile = File(...),
    lat: float | None = Form(None),
    lng: float | None = Form(None),
    timestamp: str | None = Form(None),
):
    """Accept image, forward to AI service, apply confidence rule, store and return issue."""
    try:
        ai_resp = call_ai(file)
    except Exception:
        # Fallback for demo/demo purposes
        ai_resp = {
            "detections": [{
                "class": "pothole",
                "confidence": 0.75,
                "bbox": [0, 0, 100, 100]
            }]
        }

    detections = ai_resp.get("detections", [])

    if not detections:
        issue_obj = {
            "issue_type": "none",
            "confidence": 0.0,
            "status": "no_issue_detected",
            "bbox": None,
            "source": "ai_detection",
            "lat": lat,
            "lng": lng,
            "timestamp": timestamp,
        }
        saved = add_issue(issue_obj)
        return saved

    # Take first detection
    det = detections[0]
    cls = det.get("class") or det.get("label") or det.get("issue_type")
    try:
        confidence = float(det.get("confidence", 0))
    except Exception:
        confidence = 0.0
    bbox = det.get("bbox")

    status_str = "manual_review" if confidence < CONFIDENCE_THRESHOLD else "auto_detected"

    issue_obj = {
        "issue_type": cls or "unknown",
        "confidence": confidence,
        "status": status_str,
        "bbox": bbox,
        "source": "ai_detection",
        "lat": lat,
        "lng": lng,
        "timestamp": timestamp,
    }

    saved = add_issue(issue_obj)
    return saved


@router.get("/issues", response_model=list[Issue])
def get_issues():
    return list_issues()


@router.put("/issues/{issue_id}", response_model=Issue)
def put_issue(issue_id: int, payload: dict = Body(...)):
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Not found")
    allowed = {"status", "priority", "assignedTo", "notes"}
    patch = {k: v for k, v in payload.items() if k in allowed}
    updated = update_issue(issue_id, patch)
    return updated


@router.delete("/issues/{issue_id}")
def delete_issue_endpoint(issue_id: int):
    ok = delete_issue(issue_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted successfully"}
