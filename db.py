from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Optional

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./smart_city.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple in-memory storage for issues (MVP)
_ISSUES: List[Dict] = []


def add_issue(data: Dict) -> Dict:
    new_id = len(_ISSUES) + 1
    data["id"] = new_id
    _ISSUES.append(data)
    return data


def list_issues() -> List[Dict]:
    return _ISSUES


def get_issue(issue_id: int) -> Optional[Dict]:
    for it in _ISSUES:
        if it.get("id") == issue_id:
            return it
    return None


def update_issue(issue_id: int, patch: Dict) -> Optional[Dict]:
    issue = get_issue(issue_id)
    if not issue:
        return None
    issue.update(patch)
    return issue


def delete_issue(issue_id: int) -> bool:
    for i, it in enumerate(_ISSUES):
        if it.get("id") == issue_id:
            del _ISSUES[i]
            return True
    return False
