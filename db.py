from typing import List, Dict, Optional

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
